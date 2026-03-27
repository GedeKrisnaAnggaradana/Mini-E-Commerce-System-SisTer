from flask import Flask, request, jsonify

app = Flask(__name__)

# Anda mengubah tarif dasar menjadi Rp25.000 per kilogram
BASE_RATE = 25000.0 
ZONE_MULTIPLIER = {"local": 1.0, "national": 2.0, "international": 5.0}
TYPE_MULTIPLIER = {"regular": 1.0, "express": 2.5}
DELIVERY_DAYS = {
    ("local", "regular"): "2-3 hari kerja",
    ("local", "express"): "1 hari kerja",
    ("national", "regular"): "3-5 hari kerja",
    ("national", "express"): "1-2 hari kerja",
    ("international", "regular"): "7-14 hari kerja",
    ("international", "express"): "3-5 hari kerja"
}

@app.route("/api/shipping")
def calculate_shipping():
    weight = float(request.args.get("weight", 0))
    zone = request.args.get("zone", "local")
    stype = request.args.get("type", "regular")

    zone_mult = ZONE_MULTIPLIER.get(zone, 1.0)
    type_mult = TYPE_MULTIPLIER.get(stype, 1.0)

    cost = round(weight * BASE_RATE * zone_mult * type_mult, 2)
    mode = "basic" if zone == "local" and stype == "regular" else "zone + type"

    return jsonify({
        "weight": weight,
        "zone": zone,
        "type": stype,
        "cost": cost,
        "estimated_days": DELIVERY_DAYS.get((zone, stype)),
        "mode": mode
    })

@app.route("/api/shipping/options")
def shipping_options():
    return jsonify({
        "zones": list(ZONE_MULTIPLIER.keys()),
        "types": list(TYPE_MULTIPLIER.keys()),
        "base_rate_per_kg": BASE_RATE
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)