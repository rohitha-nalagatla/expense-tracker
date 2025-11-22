"""
Database Models for Personal Expense Tracking System
SQLAlchemy ORM Models based on ER Diagram from Synopsis
"""
from datetime import datetime, date
from decimal import Decimal
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    """User model for authentication and data ownership."""
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    expenses = db.relationship('Expense', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    budgets = db.relationship('Budget', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    income_entries = db.relationship('Income', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def get_id(self):
        """Override UserMixin get_id method."""
        return str(self.user_id)
    
    def set_password(self, password):
        """Hash and set user password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash."""
        return check_password_hash(self.password_hash, password)
    
    def get_expenses_by_month(self, year, month):
        """Get expenses for a specific month."""
        return self.expenses.filter(
            db.extract('year', Expense.expense_date) == year,
            db.extract('month', Expense.expense_date) == month
        ).all()
    
    def get_total_expenses_by_category(self, year=None, month=None):
        """Get total expenses grouped by category."""
        query = db.session.query(
            Category.name,
            db.func.sum(Expense.amount).label('total')
        ).join(Expense).join(Category).filter(Expense.user_id == self.user_id)
        
        if year:
            query = query.filter(db.extract('year', Expense.expense_date) == year)
        if month:
            query = query.filter(db.extract('month', Expense.expense_date) == month)
            
        return query.group_by(Category.name).all()
    
    def __repr__(self):
        return f'<User {self.username}>'

class Category(db.Model):
    """Category model for expense classification."""
    __tablename__ = 'categories'
    
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    type = db.Column(db.String(20), nullable=False, default='expense')  # 'expense' or 'income'
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    expenses = db.relationship('Expense', backref='category', lazy='dynamic')
    budgets = db.relationship('Budget', backref='category', lazy='dynamic')
    
    @staticmethod
    def get_expense_categories():
        """Get all expense categories."""
        return Category.query.filter_by(type='expense').all()
    
    @staticmethod
    def get_income_categories():
        """Get all income categories."""
        return Category.query.filter_by(type='income').all()
    
    def __repr__(self):
        return f'<Category {self.name}>'

class Expense(db.Model):
    """Expense model for tracking expenditures."""
    __tablename__ = 'expenses'
    
    expense_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.Text)
    expense_date = db.Column(db.Date, nullable=False, default=date.today)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Expense {self.description}: ${self.amount}>'

class Income(db.Model):
    """Income model for tracking earnings."""
    __tablename__ = 'income'
    
    income_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.Text)
    income_date = db.Column(db.Date, nullable=False, default=date.today)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    category = db.relationship('Category', backref='income_entries')
    
    def __repr__(self):
        return f'<Income {self.description}: ${self.amount}>'

class Budget(db.Model):
    """Budget model for expense planning and monitoring."""
    __tablename__ = 'budgets'
    
    budget_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    month = db.Column(db.Integer, nullable=False)  # 1-12
    year = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique constraint for user + category + month + year
    __table_args__ = (
        db.UniqueConstraint('user_id', 'category_id', 'month', 'year', 
                           name='_user_category_month_year_uc'),
    )
    
    def get_spent_amount(self):
        """Calculate total spent for this budget period."""
        spent = db.session.query(db.func.sum(Expense.amount)).filter(
            Expense.user_id == self.user_id,
            Expense.category_id == self.category_id,
            db.extract('month', Expense.expense_date) == self.month,
            db.extract('year', Expense.expense_date) == self.year
        ).scalar()
        return spent or Decimal('0.00')
    
    def get_remaining_amount(self):
        """Calculate remaining budget amount."""
        return self.amount - self.get_spent_amount()
    
    def get_percentage_used(self):
        """Calculate percentage of budget used."""
        spent = self.get_spent_amount()
        if self.amount > 0:
            return float((spent / self.amount) * 100)
        return 0.0
    
    def is_over_budget(self):
        """Check if spending exceeds budget."""
        return self.get_spent_amount() > self.amount
    
    def __repr__(self):
        return f'<Budget {self.category.name} {self.month}/{self.year}: ${self.amount}>'