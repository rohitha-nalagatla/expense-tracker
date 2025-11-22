"""
Main Blueprint for Personal Expense Tracking System
Home page and dashboard routes
"""
from flask import Blueprint

bp = Blueprint('main', __name__)

from app.main import routes