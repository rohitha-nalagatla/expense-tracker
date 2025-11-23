from db import db

class Expense(db.Model):
    __tablename__ = 'expenses'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.Date, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    user_id = db.Column(db.String(30), db.ForeignKey('users.username'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    category = db.relationship('Category', backref=db.backref('expenses', lazy=True))
    user = db.relationship('User', backref=db.backref('expenses', lazy=True))

    def __repr__(self):
        return f'<Expense {self.amount} on {self.date}>'