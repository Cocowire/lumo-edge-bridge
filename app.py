from flask import Flask, request, jsonify
from datetime import datetime, timezone

app = Flask(__name__)

ALLOWED_SYMBOLS = {
    "XAUUSD.m",
    "BTCUSD.m",
    "XAGUSD.m",
    "BTCXAU.m",
}

@app.get("/")
def home():
    return jsonify({
        "status": "online",
        "system": "Lumo Edge V3.2 Bridge",
        "mode": "DEMO_SIGNAL_RECEIVER_ONLY"
    }), 200


@app.post("/webhook")
def webhook():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "ok": False,
            "error": "Invalid JSON"
        }), 400

    required = [
        "system",
        "action",
        "symbol",
        "lot",
        "price",
        "sl",
        "tp",
        "magic",
        "bar_time"
    ]

    missing = [key for key in required if key not in data]

    if missing:
        return jsonify({
            "ok": False,
            "error": "Missing fields",
            "missing": missing
        }), 400

    if data["system"] != "Lumo Edge V3.2":
        return jsonify({
            "ok": False,
            "error": "Unknown system"
        }), 400

    if data["action"] not in ("buy", "sell"):
        return jsonify({
            "ok": False,
            "error": "Invalid action"
        }), 400

    if data["symbol"] not in ALLOWED_SYMBOLS:
        return jsonify({
            "ok": False,
            "error": "Symbol not allowed"
        }), 400

    received_at = datetime.now(timezone.utc).isoformat()

    print("=" * 60)
    print("LUMO EDGE SIGNAL RECEIVED")
    print("Received:", received_at)
    print("Action:", data["action"])
    print("Symbol:", data["symbol"])
    print("Lot:", data["lot"])
    print("Price:", data["price"])
    print("SL:", data["sl"])
    print("TP:", data["tp"])
    print("Magic:", data["magic"])
    print("Bar time:", data["bar_time"])
    print("=" * 60)

    return jsonify({
        "ok": True,
        "status": "SIGNAL_RECEIVED",
        "mode": "DEMO_SIGNAL_RECEIVER_ONLY",
        "symbol": data["symbol"],
        "action": data["action"],
        "received_at": received_at
    }), 200


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=10000
    )
