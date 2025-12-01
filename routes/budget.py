from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from models import User, Category, Budget, Expense
from schemas.budget import BudgetSchema, UpdateBudgetSchema
from sqlalchemy import func
from datetime import datetime

budget_bp = Blueprint('budget', __name__, description='Budget related operations')
@budget_bp.route('/api/budgets')
class BudgetAPI(MethodView):
    @budget_bp.arguments(BudgetSchema)
    @budget_bp.response(201, BudgetSchema)
    @jwt_required()
    def post(self, args):
        current_user = get_jwt_identity()
        user = User.query.get(current_user)
        if not user:
            return {"message": "User not found"}, 404
        category = Category.query.get(args['category_id'])
        if not category:
            return {"message": "Category not found"}, 404
        if category.category_type.lower() != 'expense':
            return {"message": "Category type mismatch. Please use an expense category."}, 400
        
        # Check for duplicate budget
        existing_budget = Budget.query.filter_by(
            user_id=current_user,
            category_id=args['category_id'],
            month=args['month'],
            year=args['year']
        ).first()
        
        if existing_budget:
            return {"message": f"Budget already exists for {category.category_name} in {args['month']}/{args['year']}"}, 409
        
        budget = Budget(
            user_id=current_user,
            category_id=args['category_id'],
            amount=args['amount'],
            month=args['month'],
            year=args['year']
        )
        db.session.add(budget)
        db.session.commit()
        return budget

@budget_bp.route('/api/budgets/update')
class UpdateBudgetAPI(MethodView):
    @budget_bp.arguments(UpdateBudgetSchema)
    @budget_bp.response(200, BudgetSchema)
    @jwt_required()
    def put(self, args):
        current_user = get_jwt_identity()
        user = User.query.get(current_user)
        if not user:
            return {"message": "User not found"}, 404
        budget = Budget.query.filter_by(id=args['id'], user_id=current_user).first()
        if not budget:
            return {"message": "Budget not found"}, 404
        category = Category.query.get(args['category_id'])
        if not category:
            return {"message": "Category not found"}, 404
        if category.category_type.lower() != 'expense':
            return {"message": "Category type mismatch. Please use an expense category."}, 400
        budget.category_id = args['category_id']
        budget.amount = args['amount']
        budget.month = args['month']
        budget.year = args['year']
        db.session.commit()
        return budget

@budget_bp.route('/api/budgets/delete/<int:budget_id>')
class DeleteBudgetAPI(MethodView):
    @jwt_required()
    def delete(self, budget_id):
        """Delete a budget"""
        current_user = get_jwt_identity()
        user = User.query.get(current_user)
        if not user:
            return {"message": "User not found"}, 404
        
        budget = Budget.query.filter_by(id=budget_id, user_id=current_user).first()
        if not budget:
            return {"message": "Budget not found"}, 404
        
        db.session.delete(budget)
        db.session.commit()
        return {"message": "Budget deleted successfully"}, 200

@budget_bp.route('/api/budgets/alerts')
class BudgetAlertsAPI(MethodView):
    @jwt_required()
    def get(self):
        """Get budget alerts for current user showing categories where spending exceeds budget"""
        current_user = get_jwt_identity()
        user = User.query.get(current_user)
        if not user:
            return {"message": "User not found"}, 404
        
        # Get month and year from query params or use current
        month = request.args.get('month', type=int, default=datetime.now().month)
        year = request.args.get('year', type=int, default=datetime.now().year)
        
        # Get all budgets for user in specified month/year
        budgets = Budget.query.filter_by(
            user_id=current_user,
            month=month,
            year=year
        ).all()
        
        alerts = []
        for budget in budgets:
            # Calculate total expenses for this category in this month/year
            total_expenses = db.session.query(func.sum(Expense.amount)).filter(
                Expense.user_id == current_user,
                Expense.category_id == budget.category_id,
                func.extract('month', Expense.date) == month,
                func.extract('year', Expense.date) == year
            ).scalar() or 0
            
            # Check if expenses exceed budget
            if total_expenses > budget.amount:
                percentage_over = ((total_expenses - budget.amount) / budget.amount) * 100
                alerts.append({
                    "category_id": budget.category_id,
                    "category_name": budget.category.category_name,
                    "budget_amount": budget.amount,
                    "actual_spent": total_expenses,
                    "over_budget": total_expenses - budget.amount,
                    "percentage_over": round(percentage_over, 2),
                    "month": month,
                    "year": year,
                    "alert_level": "critical" if percentage_over > 50 else "warning"
                })
        
        return jsonify({
            "alerts": alerts,
            "total_alerts": len(alerts),
            "month": month,
            "year": year
        }), 200

@budget_bp.route('/api/budgets/summary')
class BudgetSummaryAPI(MethodView):
    @jwt_required()
    def get(self):
        """Get budget summary showing budget vs actual for all categories"""
        current_user = get_jwt_identity()
        user = User.query.get(current_user)
        if not user:
            return {"message": "User not found"}, 404
        
        month = request.args.get('month', type=int, default=datetime.now().month)
        year = request.args.get('year', type=int, default=datetime.now().year)
        
        budgets = Budget.query.filter_by(
            user_id=current_user,
            month=month,
            year=year
        ).all()
        
        summary = []
        total_budget = 0
        total_spent = 0
        
        for budget in budgets:
            total_expenses = db.session.query(func.sum(Expense.amount)).filter(
                Expense.user_id == current_user,
                Expense.category_id == budget.category_id,
                func.extract('month', Expense.date) == month,
                func.extract('year', Expense.date) == year
            ).scalar() or 0
            
            remaining = budget.amount - total_expenses
            percentage_used = (total_expenses / budget.amount * 100) if budget.amount > 0 else 0
            
            total_budget += budget.amount
            total_spent += total_expenses
            
            summary.append({
                "id": budget.id,
                "category_id": budget.category_id,
                "category_name": budget.category.category_name,
                "budget_amount": budget.amount,
                "spent_amount": total_expenses,
                "remaining_amount": remaining,
                "percentage_used": round(percentage_used, 2),
                "is_over_budget": total_expenses > budget.amount
            })
        
        return jsonify({
            "summary": summary,
            "total_budget": total_budget,
            "total_spent": total_spent,
            "total_remaining": total_budget - total_spent,
            "month": month,
            "year": year
        }), 200
