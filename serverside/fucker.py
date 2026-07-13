import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_PATH = "pico_data.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS pico_values (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                value INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

@app.route("/log", methods=["POST"])
def log_value():
    data = request.get_json(silent=True)
    if not data or "value" not in data:
        return jsonify({"error": "missing value"}), 400

    try:
        value = int(data["value"])
    except (TypeError, ValueError):
        return jsonify({"error": "value must be an integer"}), 400

    if value not in (0, 1):
        return jsonify({"error": "value must be 0 or 1"}), 400

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("INSERT INTO pico_values (value) VALUES (?)", (value,))
    return jsonify({"status": "ok"}), 201

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)