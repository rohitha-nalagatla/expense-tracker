from flask import Flask
from db import db
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from models import Budget, Category, Expense, Income, User

load_dotenv()


migrate = Migrate()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

db.init_app(app)
migrate.init_app(app, db)

if __name__ == "__main__":
    app.run(debug=True, port=8080)  # You can change the port as needed
