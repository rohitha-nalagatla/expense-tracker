from db import db


from sqlalchemy import UniqueConstraint

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(100), nullable=False)
    category_type = db.Column(db.String(50), nullable=False)  # e.g., 'Income' or 'Expense'
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    __table_args__ = (
        UniqueConstraint('category_name', 'category_type', name='uix_category_name_type'),
    )

    def __repr__(self):
        return f'<Category {self.category_name}>'
