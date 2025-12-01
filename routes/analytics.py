from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from models import User, Expense, Income, Category
from sqlalchemy import func, extract
from datetime import datetime, timedelta
from collections import defaultdict

analytics_bp = Blueprint('analytics', __name__, description='Analytics and charts operations')

@analytics_bp.route('/api/analytics/expenses-by-category')
class ExpensesByCategoryAPI(MethodView):
    @jwt_required()
    def get(self):
        """Get total expenses grouped by category for a specific period"""
        current_user = get_jwt_identity()
        user = User.query.get(current_user)
        if not user:
            return {"message": "User not found"}, 404
        
        # Get query parameters
        month = request.args.get('month', type=int)
        year = request.args.get('year', type=int)
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Build query
        query = db.session.query(
            Category.category_name,
            Category.id,
            func.sum(Expense.amount).label('total')
        ).join(Expense, Expense.category_id == Category.id).filter(
            Expense.user_id == current_user
        )
        
        # Apply date filters
        if month and year:
            query = query.filter(
                extract('month', Expense.date) == month,
                extract('year', Expense.date) == year
            )
        elif start_date and end_date:
            query = query.filter(
                Expense.date >= start_date,
                Expense.date <= end_date
            )
        
        results = query.group_by(Category.id, Category.category_name).all()
        
        data = [{
            "category_name": row[0],
            "category_id": row[1],
            "total_amount": float(row[2]) if row[2] else 0
        } for row in results]
        
        total = sum(item['total_amount'] for item in data)
        
        return jsonify({
            "data": data,
            "total": total,
            "filters": {
                "month": month,
                "year": year,
                "start_date": start_date,
                "end_date": end_date
            }
        }), 200

@analytics_bp.route('/api/analytics/income-by-category')
class IncomeByCategoryAPI(MethodView):
    @jwt_required()
    def get(self):
        """Get total income grouped by category for a specific period"""
        current_user = get_jwt_identity()
        user = User.query.get(current_user)
        if not user:
            return {"message": "User not found"}, 404
        
        month = request.args.get('month', type=int)
        year = request.args.get('year', type=int)
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = db.session.query(
            Category.category_name,
            Category.id,
            func.sum(Income.amount).label('total')
        ).join(Income, Income.category_id == Category.id).filter(
            Income.user_id == current_user
        )
        
        if month and year:
            query = query.filter(
                extract('month', Income.date) == month,
                extract('year', Income.date) == year
            )
        elif start_date and end_date:
            query = query.filter(
                Income.date >= start_date,
                Income.date <= end_date
            )
        
        results = query.group_by(Category.id, Category.category_name).all()
        
        data = [{
            "category_name": row[0],
            "category_id": row[1],
            "total_amount": float(row[2]) if row[2] else 0
        } for row in results]
        
        total = sum(item['total_amount'] for item in data)
        
        return jsonify({
            "data": data,
            "total": total,
            "filters": {
                "month": month,
                "year": year,
                "start_date": start_date,
                "end_date": end_date
            }
        }), 200

@analytics_bp.route('/api/analytics/monthly-trends')
class MonthlyTrendsAPI(MethodView):
    @jwt_required()
    def get(self):
        """Get monthly expense and income trends for the past N months"""
        current_user = get_jwt_identity()
        user = User.query.get(current_user)
        if not user:
            return {"message": "User not found"}, 404
        
        months = request.args.get('months', type=int, default=6)
        year = request.args.get('year', type=int, default=datetime.now().year)
        
        # Get expenses by month
        expense_query = db.session.query(
            extract('month', Expense.date).label('month'),
            extract('year', Expense.date).label('year'),
            func.sum(Expense.amount).label('total')
        ).filter(
            Expense.user_id == current_user,
            extract('year', Expense.date) == year
        ).group_by('month', 'year').all()
        
        # Get income by month
        income_query = db.session.query(
            extract('month', Income.date).label('month'),
            extract('year', Income.date).label('year'),
            func.sum(Income.amount).label('total')
        ).filter(
            Income.user_id == current_user,
            extract('year', Income.date) == year
        ).group_by('month', 'year').all()
        
        # Organize data
        expenses_by_month = {int(row[0]): float(row[2]) for row in expense_query}
        income_by_month = {int(row[0]): float(row[2]) for row in income_query}
        
        trends = []
        for month in range(1, 13):
            expense_amount = expenses_by_month.get(month, 0)
            income_amount = income_by_month.get(month, 0)
            trends.append({
                "month": month,
                "month_name": datetime(year, month, 1).strftime("%B"),
                "year": year,
                "expenses": expense_amount,
                "income": income_amount,
                "net": income_amount - expense_amount
            })
        
        return jsonify({
            "trends": trends,
            "year": year
        }), 200

@analytics_bp.route('/api/analytics/dashboard-summary')
class DashboardSummaryAPI(MethodView):
    @jwt_required()
    def get(self):
        """Get comprehensive dashboard summary with all key metrics"""
        current_user = get_jwt_identity()
        user = User.query.get(current_user)
        if not user:
            return {"message": "User not found"}, 404
        
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        # Total expenses this month
        total_expenses_month = db.session.query(func.sum(Expense.amount)).filter(
            Expense.user_id == current_user,
            extract('month', Expense.date) == current_month,
            extract('year', Expense.date) == current_year
        ).scalar() or 0
        
        # Total income this month
        total_income_month = db.session.query(func.sum(Income.amount)).filter(
            Income.user_id == current_user,
            extract('month', Income.date) == current_month,
            extract('year', Income.date) == current_year
        ).scalar() or 0
        
        # Total expenses all time
        total_expenses_all = db.session.query(func.sum(Expense.amount)).filter(
            Expense.user_id == current_user
        ).scalar() or 0
        
        # Total income all time
        total_income_all = db.session.query(func.sum(Income.amount)).filter(
            Income.user_id == current_user
        ).scalar() or 0
        
        # Recent expenses (last 5)
        recent_expenses = Expense.query.filter_by(user_id=current_user).order_by(
            Expense.date.desc()
        ).limit(5).all()
        
        # Recent income (last 5)
        recent_income = Income.query.filter_by(user_id=current_user).order_by(
            Income.date.desc()
        ).limit(5).all()
        
        return jsonify({
            "current_month": {
                "total_expenses": float(total_expenses_month),
                "total_income": float(total_income_month),
                "net_balance": float(total_income_month - total_expenses_month),
                "month": current_month,
                "year": current_year
            },
            "all_time": {
                "total_expenses": float(total_expenses_all),
                "total_income": float(total_income_all),
                "net_balance": float(total_income_all - total_expenses_all)
            },
            "recent_expenses": [{
                "id": exp.id,
                "amount": exp.amount,
                "description": exp.description,
                "category_name": exp.category.category_name,
                "date": exp.date.isoformat()
            } for exp in recent_expenses],
            "recent_income": [{
                "id": inc.id,
                "amount": inc.amount,
                "description": inc.description,
                "category_name": inc.category.category_name,
                "date": inc.date.isoformat()
            } for inc in recent_income]
        }), 200

@analytics_bp.route('/api/analytics/category-comparison')
class CategoryComparisonAPI(MethodView):
    @jwt_required()
    def get(self):
        """Compare expenses across different time periods for a category"""
        current_user = get_jwt_identity()
        user = User.query.get(current_user)
        if not user:
            return {"message": "User not found"}, 404
        
        category_id = request.args.get('category_id', type=int)
        if not category_id:
            return {"message": "category_id is required"}, 400
        
        # Get last 6 months of data for this category
        results = []
        current_date = datetime.now()
        
        for i in range(6):
            month = ((current_date.month - i - 1) % 12) + 1
            year = current_date.year if current_date.month - i > 0 else current_date.year - 1
            
            total = db.session.query(func.sum(Expense.amount)).filter(
                Expense.user_id == current_user,
                Expense.category_id == category_id,
                extract('month', Expense.date) == month,
                extract('year', Expense.date) == year
            ).scalar() or 0
            
            results.insert(0, {
                "month": month,
                "year": year,
                "month_name": datetime(year, month, 1).strftime("%B %Y"),
                "total": float(total)
            })
        
        return jsonify({
            "category_id": category_id,
            "comparison": results
        }), 200
