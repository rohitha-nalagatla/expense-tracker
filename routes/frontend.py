from flask import Blueprint, render_template, redirect, url_for, session, request
from functools import wraps

frontend_bp = Blueprint('frontend', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'access_token' not in session:
            return redirect(url_for('frontend.login'))
        return f(*args, **kwargs)
    return decorated_function

@frontend_bp.route('/')
def index():
    """Landing page"""
    if 'access_token' in session:
        return redirect(url_for('frontend.dashboard'))
    return render_template('index.html')

@frontend_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        data = request.get_json()
        session['access_token'] = data.get('access_token')
        session['username'] = data.get('username')
        return {'status': 'ok'}, 200
    return render_template('auth/login.html')

@frontend_bp.route('/register')
def register():
    """Register page"""
    return render_template('auth/register.html')

@frontend_bp.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard"""
    return render_template('dashboard.html', username=session.get('username'))

@frontend_bp.route('/expenses')
@login_required
def expenses():
    """Expenses management page"""
    return render_template('expenses.html', username=session.get('username'))

@frontend_bp.route('/income')
@login_required
def income():
    """Income management page"""
    return render_template('income.html', username=session.get('username'))

@frontend_bp.route('/budgets')
@login_required
def budgets():
    """Budget management page"""
    return render_template('budgets.html', username=session.get('username'))

@frontend_bp.route('/analytics')
@login_required
def analytics():
    """Analytics and charts page"""
    return render_template('analytics.html', username=session.get('username'))

@frontend_bp.route('/logout')
def logout():
    """Logout and clear session"""
    session.clear()
    return redirect(url_for('frontend.login'))
