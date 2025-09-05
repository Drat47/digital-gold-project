from app.models import db, Investment
from app.app import app

with app.app_context():
    inv1 = Investment(base_amount=5000, gst_paid=90, platform_fee_percent=2, buy_price_per_gram=6000, grams=0.83)
    inv2 = Investment(base_amount=10000, gst_paid=180, platform_fee_percent=2, buy_price_per_gram=6100, grams=1.63)
    db.session.add_all([inv1, inv2])
    db.session.commit()
    print("✅ Seed data inserted successfully!")
