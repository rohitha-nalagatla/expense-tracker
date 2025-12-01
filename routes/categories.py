from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required,get_jwt_identity
from db import db
from models import Category, User


category_bp = Blueprint('category', __name__, description='Category related operations')

@category_bp.route('/api/categories/type/<string:category_type>')
class CategoryByTypeAPI(MethodView):
    @jwt_required()
    def get(self, category_type):
        current_user = get_jwt_identity()
        user = User.query.get(current_user)
        if not user:
            return {"message": "User not found"}, 404
        if not category_type.lower() in ['income', 'expense']:
            return {"message": "Invalid category type. Must be 'Income' or 'Expense'."}, 400
        categories = Category.query.filter_by(category_type=category_type).all()
        if not categories:
            return {"message": "No categories found for the specified type"}, 404
        return jsonify([{
            "category_name": category.category_name,
            "category_type": category.category_type
        } for category in categories]), 200

@category_bp.route('/api/categories')
class AllCategoriesAPI(MethodView):
    @jwt_required()
    def get(self):
        """Get all categories"""
        current_user = get_jwt_identity()
        user = User.query.get(current_user)
        if not user:
            return {"message": "User not found"}, 404
        
        categories = Category.query.all()
        return jsonify([{
            "id": category.id,
            "category_name": category.category_name,
            "category_type": category.category_type
        } for category in categories]), 200
