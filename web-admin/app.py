from flask import Flask, render_template
import requests
import os

app = Flask(__name__)

# Sistem menghubungi kontainer lain menggunakan host.docker.internal
SERVICE_A_URL = "http://host.docker.internal:8081/api/products"
SERVICE_B_URL = "http://host.docker.internal:8082/api/shipping/options"

@app.route("/")
def admin_dashboard():
    products_data = []
    shipping_data = {}
    
    # Blok pengambilan data katalog dari Service A
    try:
        prod_resp = requests.get(SERVICE_A_URL)
        if prod_resp.status_code == 200:
            products_data = prod_resp.json()
    except requests.exceptions.RequestException:
        pass
        
    # Blok pengambilan data tarif dari Service B
    try:
        ship_resp = requests.get(SERVICE_B_URL)
        if ship_resp.status_code == 200:
            shipping_data = ship_resp.json()
    except requests.exceptions.RequestException:
        pass

    # Sistem menyisipkan variabel ke dalam templat HTML
    return render_template("admin.html", products=products_data, shipping=shipping_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)