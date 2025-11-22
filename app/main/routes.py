"""
Main Routes for Personal Expense Tracking System
Dashboard, home page, and overview routes
"""
from datetime import datetime, date
from flask import render_template, request, jsonify
from flask_login import login_required, current_user
from app.main import bp
from app.models import Expense, Category, Budget, Income
from app import db

@bp.route('/')
@bp.route('/index')
def index():
    """Home page route."""
    if current_user.is_authenticated:
        return render_template('dashboard.html', title='Dashboard')
    return render_template('index.html', title='Welcome')

@bp.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard with financial overview."""
    # Get current month data
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    # Get monthly expenses
    monthly_expenses = current_user.get_expenses_by_month(current_year, current_month)
    total_monthly_expenses = sum([exp.amount for exp in monthly_expenses])
    
    # Get monthly income
    monthly_income = db.session.query(Income).filter(
        Income.user_id == current_user.user_id,
        db.extract('month', Income.income_date) == current_month,
        db.extract('year', Income.income_date) == current_year
    ).all()
    total_monthly_income = sum([inc.amount for inc in monthly_income])
    
    # Get category breakdown
    category_breakdown = current_user.get_total_expenses_by_category(current_year, current_month)
    
    # Get recent expenses (last 5)
    recent_expenses = Expense.query.filter_by(user_id=current_user.user_id)\
        .order_by(Expense.created_at.desc()).limit(5).all()
    
    # Get budget status
    budgets = Budget.query.filter(
        Budget.user_id == current_user.user_id,
        Budget.month == current_month,
        Budget.year == current_year
    ).all()
    
    budget_status = []
    for budget in budgets:
        status = {
            'category': budget.category.name,
            'budgeted': float(budget.amount),
            'spent': float(budget.get_spent_amount()),
            'remaining': float(budget.get_remaining_amount()),
            'percentage': budget.get_percentage_used(),
            'over_budget': budget.is_over_budget()
        }
        budget_status.append(status)
    
    return render_template('dashboard.html',
                         title='Dashboard',
                         total_monthly_expenses=total_monthly_expenses,
                         total_monthly_income=total_monthly_income,
                         net_savings=total_monthly_income - total_monthly_expenses,
                         category_breakdown=category_breakdown,
                         recent_expenses=recent_expenses,
                         budget_status=budget_status,
                         current_month=current_month,
                         current_year=current_year)

@bp.route('/api/monthly_expenses/<int:year>/<int:month>')
@login_required
def api_monthly_expenses(year, month):
    """API endpoint for monthly expense data."""
    expenses = current_user.get_expenses_by_month(year, month)
    expense_data = []
    
    for expense in expenses:
        expense_data.append({
            'date': expense.expense_date.isoformat(),
            'amount': float(expense.amount),
            'category': expense.category.name,
            'description': expense.description
        })
    
    return jsonify(expense_data)

@bp.route('/api/category_breakdown/<int:year>/<int:month>')
@login_required
def api_category_breakdown(year, month):
    """API endpoint for category breakdown chart data."""
    category_data = current_user.get_total_expenses_by_category(year, month)
    
    chart_data = {
        'labels': [cat[0] for cat in category_data],
        'data': [float(cat[1]) for cat in category_data]
    }
    
    return jsonify(chart_data)