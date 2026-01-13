from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from models import Expense, User, Category
from schemas.expenses import ExpenseSchema,UpdateExpenseSchema

expense_bp = Blueprint('expense', __name__, description='Expense related operations')

@expense_bp.route('/api/expenses')
class ExpenseAPI(MethodView):
    @expense_bp.arguments(ExpenseSchema)
    @expense_bp.response(201, ExpenseSchema)
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
        expense = Expense(
            user_id=current_user,
            category_id=args['category_id'],
            amount=args['amount'],
            description=args.get('description'),
            date=args['date']
        )
        db.session.add(expense)
        db.session.commit()
        return expense

@expense_bp.route('/api/expenses/update')
class UpdateExpenseAPI(MethodView):
    @expense_bp.arguments(UpdateExpenseSchema)
    @expense_bp.response(200, UpdateExpenseSchema)
    @jwt_required()
    def put(self, args):
        current_user = get_jwt_identity()
        user = User.query.get(current_user)
        if not user:
            return {"message": "User not found"}, 404
        expense = Expense.query.filter_by(id=args['id'], user_id=current_user).first()
        if not expense:
            return {"message": "Expense not found"}, 404
        category = Category.query.get(args['category_id'])
        if not category:
            return {"message": "Category not found"}, 404
        if category.category_type.lower() != 'expense':
            return {"message": "Category type mismatch. Please use an expense category."}, 400
        expense.category_id = args['category_id']
        expense.amount = args['amount']
        expense.description = args.get('description')
        expense.date = args['date']
        db.session.commit()
        return expense

@expense_bp.route('/api/expenses/delete/<int:expense_id>')
class DeleteExpenseAPI(MethodView):
    @jwt_required()
    def delete(self, expense_id):
        current_user = get_jwt_identity()
        user = User.query.get(current_user)
        if not user:
            return {"message": "User not found"}, 404
        expense = Expense.query.filter_by(id=expense_id, user_id=current_user).first()
        if not expense:
            return {"message": "Expense not found"}, 404
        db.session.delete(expense)
        db.session.commit()
        return {"message": "Expense deleted successfully"}, 200

@expense_bp.route('/api/expenses/user')
class UserExpensesAPI(MethodView):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        user = User.query.get(current_user)
        if not user:
            return {"message": "User not found"}, 404
        # Get optional query params
        category_id = request.args.get('category_id', type=int)
        date = request.args.get('date')  # Expecting YYYY-MM-DD
        query = Expense.query.filter_by(user_id=current_user)
        if category_id is not None:
            query = query.filter_by(category_id=category_id)
        if date is not None:
            query = query.filter_by(date=date)
        expenses = query.all()
        return jsonify([
            {
                "id": expense.id,
                "category_id": expense.category_id,
                "amount": expense.amount,
                "description": expense.description,
                "date": expense.date.isoformat()
            } for expense in expenses
        ]), 200