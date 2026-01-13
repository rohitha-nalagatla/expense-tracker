from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from models import Income, User, Category
from schemas.income import IncomeSchema,UpdateIncomeSchema

income_bp = Blueprint('income', __name__, description='Income related operations')
@income_bp.route('/api/income')
class IncomeAPI(MethodView):
    @income_bp.arguments(IncomeSchema)
    @income_bp.response(201,IncomeSchema)
    @jwt_required()
    def post(self,args):
        current_user=get_jwt_identity()
        user=User.query.get(current_user)
        if not user:
            return {"message": "User not found"}, 404
        category = Category.query.get(args['category_id'])
        if not category:
            return {"message": "Category not found"}, 404
        if category.category_type.lower() != 'income':
            return {"message": "Category type mismatch. Please use an income category."}, 400
        income = Income(
            user_id=current_user,
            category_id=args['category_id'],
            amount=args['amount'],
            description=args.get('description'),
            date=args['date']
        )
        db.session.add(income)
        db.session.commit()
        return income


@income_bp.route('/api/income/update')
class IncomeUpdateAPI(MethodView):
    @income_bp.arguments(UpdateIncomeSchema)
    @income_bp.response(201,UpdateIncomeSchema)   
    @jwt_required()
    def put(self,args):
        current_user=get_jwt_identity()
        user=User.query.get(current_user)   
        if not user:
            return {"message": "User not found"}, 404
        income=Income.query.filter_by(id=args['id'],user_id=current_user).first()
        if not income:
            return {"message":"income not found"},404
        category=Category.query.get(args['category_id'])
        if not category:
            return {"message":"Category not found"},404
        if category.category_type.lower() != 'income':
            return {"message": "Category type mismatch. Please use an income category."}, 400
        income.category_id=args['category_id']
        income.amount=args['amount']
        income.description=args.get('description')
        income.date=args['date']
        db.session.commit()
        return income

@income_bp.route('/api/income/delete/<int:income_id>')
class DeleteIncomeAPI(MethodView):
    @jwt_required()
    def delete(self,income_id):
        current_user=get_jwt_identity()
        user=User.query.get(current_user)   
        if not user:
            return {"message": "User not found"}, 404
        income = Income.query.filter_by(id=income_id, user_id=current_user).first()
        if not income:
            return {"message": "income not found"}, 404
        db.session.delete(income)
        db.session.commit()
        return {"message": "Income deleted successfully"}, 200

@income_bp.route('/api/income/user')
class UserIncomeAPI(MethodView):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        user = User.query.get(current_user)
        if not user:
            return {"message": "User not found"}, 404
        # Get optional query params
        category_id = request.args.get('category_id', type=int)
        date = request.args.get('date')  # Expecting YYYY-MM-DD
        query = Income.query.filter_by(user_id=current_user)
        if category_id is not None:
            query = query.filter_by(category_id=category_id)
        if date is not None:
            query = query.filter_by(date=date)
        incomes = query.all()
        return jsonify([
            {
                "id": income.id,
                "category_id": income.category_id,
                "amount": income.amount,
                "description": income.description,
                "date": income.date.isoformat()
            } for income in incomes
        ]), 200




