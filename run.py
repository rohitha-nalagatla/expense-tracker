"""
Personal Expense Tracking System - Main Application
Entry point for the Flask application
"""
from app import create_app, db
from flask_migrate import Migrate

# Create the Flask application
app = create_app()
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    """Make database models available in Flask shell."""
    from app.models import User, Expense, Category, Budget
    return {'db': db, 'User': User, 'Expense': Expense, 'Category': Category, 'Budget': Budget}

if __name__ == '__main__':
    app.run(debug=True)