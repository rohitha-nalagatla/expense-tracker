from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from models import User
from schemas.user import UserRegisterSchema, UserLoginSchema, UserResponseSchema


user_bp = Blueprint('user', __name__, description='User related operations')

@user_bp.route('/api/users/register')
class UserRegisterAPI(MethodView):
    @user_bp.arguments(UserRegisterSchema)
    def post(self, args):
        if User.query.filter_by(username=args['username']).first() or User.query.filter_by(email=args['email']).first():
            return {"message": "User already exists"}, 400
        hashed_password = generate_password_hash(args['password'])
        user = User(
            username=args['username'],
            email=args['email'],
            password_hash=hashed_password,
            full_name=args.get('full_name'),
            age=args.get('age')
        )
        db.session.add(user)
        db.session.commit()
        return {"message": "User registered successfully"}, 201

@user_bp.route('/api/users/login')
class UserLoginAPI(MethodView):
    @user_bp.arguments(UserLoginSchema)
    def post(self, args):
        user = User.query.filter_by(username=args['username']).first()
        if not user or not check_password_hash(user.password_hash, args['password']):
            return {"message": "Invalid username or password"}, 401
        access_token = create_access_token(identity=user.username)
        return {
            "message": f"Welcome {user.full_name or user.username}!",
            "access_token": access_token
        }, 200

@user_bp.route('/api/user')
class UserInfoAPI(MethodView):
    @jwt_required()
    @user_bp.response(200, UserResponseSchema)
    def get(self):
        current_username = get_jwt_identity()
        user = User.query.get(current_username)
        if not user:
            return {"message": "User not found"}, 404
        return user


