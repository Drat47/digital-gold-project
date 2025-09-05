from flask import Flask, request, jsonify
from flask_migrate import Migrate
from app.models import db, Investment   # ✅ import from app.models

app = Flask(__name__)

# --- DB config ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///digital_gold.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

# ---------------- BASIC ROUTES ----------------
@app.route("/")
def home():
    return "✅ Digital Gold Backend Running!"

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "ok", "message": "server alive"})

# ---------------- DEBUG HELPERS ----------------
@app.before_request
def log_request_info():
    """Har request ka method, path, query aur body log karega."""
    body = None
    try:
        body = request.get_json(silent=True)
    except Exception:
        body = None
    print(
        f"[REQ] METHOD={request.method} "
        f"PATH={repr(request.path)} "
        f"QS={request.query_string!r} "
        f"CT={request.headers.get('Content-Type')} "
        f"BODY={body}"
    )

@app.route("/debug/echo", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def debug_echo():
    """Jo bhejoge wohi wapas milega (for testing)."""
    return jsonify({
        "method": request.method,
        "path": request.path,
        "query": request.args,
        "headers_sample": {
            "Content-Type": request.headers.get("Content-Type"),
            "User-Agent": request.headers.get("User-Agent"),
        },
        "json": request.get_json(silent=True),
    })

@app.route("/__routes__", methods=["GET"])
def list_routes():
    """App me registered saare routes dikhao."""
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({"rule": str(rule), "methods": sorted(list(rule.methods))})
    return jsonify(routes)

# ---------------- ACTUAL API ----------------
# ➤ Create new investment
@app.route('/investments', methods=['POST'])
def add_investment():
    data = request.get_json() or {}

    # grams optional hai; missing ho to calculate kar lo
    grams = data.get('grams')
    if not grams:
        grams = float(data['base_amount']) / float(data['buy_price_per_gram'])

    new_investment = Investment(
        base_amount=data['base_amount'],
        gst_paid=data['gst_paid'],
        platform_fee_percent=data.get('platform_fee_percent', 0),
        buy_price_per_gram=data['buy_price_per_gram'],
        grams=grams
    )
    db.session.add(new_investment)
    db.session.commit()
    return jsonify({"message": "Investment added successfully!"}), 201

# ➤ Get all investments
@app.route('/investments', methods=['GET'])
def get_investments():
    investments = Investment.query.all()
    result = [
        {
            "id": inv.id,
            "base_amount": inv.base_amount,
            "gst_paid": inv.gst_paid,
            "platform_fee_percent": inv.platform_fee_percent,
            "buy_price_per_gram": inv.buy_price_per_gram,
            "grams": inv.grams
        }
        for inv in investments
    ]
    return jsonify(result)

# ➤ Get one investment by ID
@app.route('/investments/<int:id>', methods=['GET'])
def get_investment(id):
    inv = Investment.query.get(id)
    if not inv:
        return jsonify({"message": "Investment not found"}), 404
    return jsonify({
        "id": inv.id,
        "base_amount": inv.base_amount,
        "gst_paid": inv.gst_paid,
        "platform_fee_percent": inv.platform_fee_percent,
        "buy_price_per_gram": inv.buy_price_per_gram,
        "grams": inv.grams
    })

# ➤ Update investment
@app.route('/investments/<int:id>', methods=['PUT'])
def update_investment(id):
    data = request.get_json() or {}
    investment = Investment.query.get(id)
    if not investment:
        return jsonify({"message": "Investment not found"}), 404

    investment.base_amount = data.get('base_amount', investment.base_amount)
    investment.gst_paid = data.get('gst_paid', investment.gst_paid)
    investment.platform_fee_percent = data.get('platform_fee_percent', investment.platform_fee_percent)
    investment.buy_price_per_gram = data.get('buy_price_per_gram', investment.buy_price_per_gram)
    investment.grams = data.get('grams', investment.grams)

    db.session.commit()
    return jsonify({"message": "Investment updated successfully!"})

# ➤ Delete investment
@app.route('/investments/<int:id>', methods=['DELETE'])
def delete_investment(id):
    investment = Investment.query.get(id)
    if not investment:
        return jsonify({"message": "Investment not found"}), 404

    db.session.delete(investment)
    db.session.commit()
    return jsonify({"message": "Investment deleted successfully!"})

# ➤ Calculate returns (simple example)
@app.route('/investments/<int:id>/returns', methods=['GET'])
def calculate_returns(id):
    investment = Investment.query.get(id)
    if not investment:
        return jsonify({"message": "Investment not found"}), 404

    current_price = 7500  # Assume current gold price
    current_value = investment.grams * current_price
    profit = current_value - investment.base_amount - investment.gst_paid

    return jsonify({
        "base_amount": investment.base_amount,
        "grams_bought": investment.grams,
        "current_price": current_price,
        "current_value": current_value,
        "profit": profit
    })

if __name__ == '__main__':
    app.run(debug=True)
