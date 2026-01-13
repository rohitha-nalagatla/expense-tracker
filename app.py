from flask import Flask
from db import db
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from models import Budget, Category, Expense, Income, User
from flask_jwt_extended import JWTManager
from routes.user import user_bp
from routes.categories import category_bp
from routes.expenses import expense_bp
from routes.income import income_bp
from routes.budget import budget_bp
load_dotenv()


migrate = Migrate()
jwt = JWTManager()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY', 'super-secret')  # Change this in production
db.init_app(app)
migrate.init_app(app, db)
jwt.init_app(app)
app.register_blueprint(user_bp)
app.register_blueprint(category_bp)
app.register_blueprint(expense_bp)
app.register_blueprint(income_bp)
app.register_blueprint(budget_bp)

if __name__ == "__main__":
    app.run(debug=True, port=8080)  # You can change the port as needed
