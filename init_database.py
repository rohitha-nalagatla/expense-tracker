"""
Auto-initialize database on first run
This ensures the database is created with all tables and default data
"""
from app import app, db
from models import Category
import os

def init_database():
    """Initialize database with tables and default categories"""
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")
        
        # Check if categories already exist
        existing_count = Category.query.count()
        if existing_count > 0:
            print(f"Database already has {existing_count} categories. Skipping initialization.")
            return
        
        print("Adding default categories...")
        
        # Add default expense categories
        expense_categories = [
            'Food & Dining',
            'Transportation',
            'Shopping',
            'Entertainment',
            'Bills & Utilities',
            'Healthcare',
            'Education',
            'Travel',
            'Groceries',
            'Other Expenses'
        ]
        
        # Add default income categories
        income_categories = [
            'Salary',
            'Freelance',
            'Business',
            'Investments',
            'Gifts',
            'Other Income'
        ]
        
        # Insert expense categories
        for cat_name in expense_categories:
            category = Category(category_name=cat_name, category_type='expense')
            db.session.add(category)
        
        # Insert income categories
        for cat_name in income_categories:
            category = Category(category_name=cat_name, category_type='income')
            db.session.add(category)
        
        db.session.commit()
        print(f"Database initialized successfully with {len(expense_categories) + len(income_categories)} default categories!")
        print(f"Database location: {app.config['SQLALCHEMY_DATABASE_URI']}")

if __name__ == '__main__':
    init_database()
