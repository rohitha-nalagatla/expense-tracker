from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from models import User, Category, Budget
from schemas.budget import BudgetSchema, UpdateBudgetSchema

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
    @budget_bp.arguments(BudgetSchema)
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