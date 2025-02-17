
# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class RentalItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"RentalItem('{self.title}', '{self.price}')"