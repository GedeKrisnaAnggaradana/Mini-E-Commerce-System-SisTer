from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

coupons = {
    "HEMAT10": {"discount_percent": 10},
    "DISKON50": {"discount_percent": 50}
}

@app.route("/api/diskon/<string:code>")
def get_discount(code):
    # Variasi 1: Logika Kupon Manual
    code = code.upper()
    coupon_data = coupons.get(code, {"discount_percent": 0})
    discount_percent = coupon_data["discount_percent"]
    message = "Kupon berhasil digunakan" if discount_percent > 0 else "Kupon tidak valid"

    # Variasi 2: Deteksi Waktu Flash Sale & Weekend
    now = datetime.now()
    current_hour = now.hour
    current_day = now.weekday()

    if current_hour == 12:
        discount_percent += 5
        message += " + Bonus Flash Sale Siang (5%)!"
    elif current_day >= 5:
        discount_percent += 10
        message += " + Bonus Happy Weekend (10%)!"

    return jsonify({
        "code": code,
        "discount_percent": discount_percent,
        "note": message,
        "server_time": now.strftime("%Y-%m-%d %H:%M:%S")
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)