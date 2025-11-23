"""
Add predefined categories

Revision ID: add_predefined_categories
Create Date: 2025-11-23
"""
from alembic import op

# revision identifiers, used by Alembic.
revision = 'add_predefined_categories'
down_revision = '55829d19073c'
branch_labels = None
depends_on = None

def upgrade():
    op.execute("""
        INSERT INTO categories (category_name, category_type, description) VALUES
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
        ('Miscellaneous', 'expense', 'Other expenses not categorized'),
        ('Salary', 'income', 'Primary employment income'),
        ('Freelance', 'income', 'Contract and freelance work'),
        ('Investment', 'income', 'Dividends, interest, capital gains'),
        ('Business', 'income', 'Business revenue and profits'),
        ('Gift', 'income', 'Gifts and monetary presents'),
        ('Other Income', 'income', 'Miscellaneous income sources')
    """)

def downgrade():
    op.execute("""
        DELETE FROM categories WHERE category_name IN (
            'Food & Dining', 'Transportation', 'Housing', 'Healthcare', 'Shopping',
            'Entertainment', 'Education', 'Bills & Utilities', 'Personal Care',
            'Travel', 'Miscellaneous', 'Salary', 'Freelance', 'Investment',
            'Business', 'Gift', 'Other Income'
        )
    """)
