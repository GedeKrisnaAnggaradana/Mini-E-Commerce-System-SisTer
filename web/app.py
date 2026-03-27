from flask import Flask, jsonify, request
import requests
import os

app = Flask(__name__)

SERVICE_A_URL = "http://host.docker.internal:8081/api/products"
SERVICE_B_URL = "http://host.docker.internal:8082/api/shipping"
SERVICE_C_URL = "http://host.docker.internal:8083/api/diskon"

def format_rupiah(angka):
    """Fungsi pembantu untuk mengubah angka menjadi format Rupiah"""
    return f"Rp {int(angka):,}".replace(",", ".")

@app.route("/checkout/<int:product_id>")
def checkout(product_id):
    coupon = request.args.get("coupon", "")
    zone = request.args.get("zone", "local")
    stype = request.args.get("type", "regular")

    try:
        product_resp = requests.get(f"{SERVICE_A_URL}/{product_id}")
        product_resp.raise_for_status()
        product = product_resp.json()
    except requests.exceptions.RequestException:
        return jsonify({"error": "Service A gagal merespons"}), 500

    try:
        shipping_resp = requests.get(
            SERVICE_B_URL,
            params={"weight": product.get("weight", 0), "zone": zone, "type": stype}
        )
        shipping_resp.raise_for_status()
        shipping = shipping_resp.json()
    except requests.exceptions.RequestException:
        return jsonify({"error": "Service B gagal merespons"}), 500

    discount_percent = 0
    if coupon:
        try:
            discount_resp = requests.get(f"{SERVICE_C_URL}/{coupon}")
            discount_resp.raise_for_status()
            discount_data = discount_resp.json()
            discount_percent = discount_data.get("discount_percent", 0)
        except requests.exceptions.RequestException:
            pass

    # Kalkulasi menggunakan angka mentah (integer/float)
    price_original = product.get("price", 0)
    shipping_cost = shipping.get("cost", 0)
    discount_saved = price_original * (discount_percent / 100)
    total_bill = price_original - discount_saved + shipping_cost

    # Sistem mengonversi hasil akhir ke format mata uang Rupiah
    return jsonify({
        "details": {
            "category": product.get("category", "unknown"),
            "estimated_days": shipping.get("estimated_days", "unknown"),
            "shipping_type": shipping.get("type", "regular"),
            "shipping_zone": shipping.get("zone", "local")
        },
        "discount_applied": f"{discount_percent}%",
        "discount_saved": format_rupiah(discount_saved),
        "price_original": format_rupiah(price_original),
        "product": product.get("name", "unknown"),
        "shipping_cost": format_rupiah(shipping_cost),
        "total_bill": format_rupiah(total_bill)
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)