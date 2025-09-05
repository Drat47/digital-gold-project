from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Investment(db.Model):
    __tablename__ = "investment"

    id = db.Column(db.Integer, primary_key=True)
    base_amount = db.Column(db.Float, nullable=False)          # User ne kitna invest kiya
    gst_paid = db.Column(db.Float, nullable=False)             # GST amount
    platform_fee_percent = db.Column(db.Float, default=0.0)    # Platform fee %
    buy_price_per_gram = db.Column(db.Float, nullable=False)   # Buy time ka gold price
    grams = db.Column(db.Float, nullable=False)                # Kitne grams gold mile
    invested_at = db.Column(db.DateTime, default=datetime.utcnow)  # Auto timestamp

    def __repr__(self):
        return f"<Investment {self.id}: {self.grams}g at {self.buy_price_per_gram}>"
