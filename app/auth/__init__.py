"""
Authentication Blueprint for Personal Expense Tracking System
Login, registration, and user management
"""
from flask import Blueprint

bp = Blueprint('auth', __name__)

from app.auth import routes