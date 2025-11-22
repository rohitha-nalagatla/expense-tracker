"""
Expenses Blueprint for Personal Expense Tracking System
Expense management, budgets, and reporting
"""
from flask import Blueprint

bp = Blueprint('expenses', __name__)

from app.expenses import routes