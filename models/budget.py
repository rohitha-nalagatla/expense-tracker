
from sqlalchemy import UniqueConstraint
from db import db

class Budget(db.Model):
    __tablename__ = 'budgets'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(30), db.ForeignKey('users.username'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    __table_args__ = (
        UniqueConstraint('user_id', 'category_id', 'month', 'year', name='uix_user_category_month_year'),
    )

    user = db.relationship('User', backref=db.backref('budgets', lazy=True))
    category = db.relationship('Category', backref=db.backref('budgets', lazy=True))

    def __repr__(self):
        return f'<Budget {self.amount} for {self.category} in {self.month}/{self.year}>'