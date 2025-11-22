"""
Data Initialization Script for Personal Expense Tracking System
Seeds the database with default categories
"""
from app import create_app, db
from app.models import Category

def init_default_categories():
    """Initialize default expense and income categories."""
    
    # Expense Categories
    expense_categories = [
        ('Food & Dining', 'expense', 'Groceries, restaurants, takeout'),
        ('Transportation', 'expense', 'Gas, public transport, ride-sharing'),
        ('Housing', 'expense', 'Rent, utilities, maintenance'),
        ('Healthcare', 'expense', 'Medical bills, insurance, medications'),
        ('Shopping', 'expense', 'Clothing, electronics, personal items'),
        ('Entertainment', 'expense', 'Movies, streaming, games, hobbies'),
        ('Education', 'expense', 'Books, courses, tuition, training'),
        ('Bills & Utilities', 'expense', 'Phone, internet, electricity, water'),
        ('Personal Care', 'expense', 'Haircuts, cosmetics, gym membership'),
        ('Travel', 'expense', 'Vacation, business trips, accommodation'),
        ('Miscellaneous', 'expense', 'Other expenses not categorized')
    ]
    
    # Income Categories
    income_categories = [
        ('Salary', 'income', 'Primary employment income'),
        ('Freelance', 'income', 'Contract and freelance work'),
        ('Investment', 'income', 'Dividends, interest, capital gains'),
        ('Business', 'income', 'Business revenue and profits'),
        ('Gift', 'income', 'Gifts and monetary presents'),
        ('Other Income', 'income', 'Miscellaneous income sources')
    ]
    
    # Combine all categories
    all_categories = expense_categories + income_categories
    
    # Add categories to database
    for name, category_type, description in all_categories:
        # Check if category already exists
        existing_category = Category.query.filter_by(name=name).first()
        if not existing_category:
            category = Category(
                name=name,
                type=category_type,
                description=description
            )
            db.session.add(category)
            print(f"Added category: {name} ({category_type})")
        else:
            print(f"Category already exists: {name}")
    
    try:
        db.session.commit()
        print("\n✅ Default categories initialized successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"\n❌ Error initializing categories: {str(e)}")

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        # Create all database tables
        db.create_all()
        print("Database tables created.")
        
        # Initialize default categories
        init_default_categories()
        
        print("\n🎉 Database initialization completed!")
        print("You can now run the application with: python run.py")