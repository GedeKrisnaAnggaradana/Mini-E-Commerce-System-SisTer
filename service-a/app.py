from flask import Flask, jsonify, request
import mysql.connector
import os
import time

app = Flask(__name__)

def get_db_connection():
    """Fungsi untuk membuat koneksi ke MySQL dengan metode Retry"""
    retries = 5
    while retries > 0:
        try:
            conn = mysql.connector.connect(
                host=os.getenv("DB_HOST", "mysql-db"), 
                user=os.getenv("DB_USER", "root"),
                password=os.getenv("DB_PASSWORD", "password"),
                database=os.getenv("DB_NAME", "catalog_db")
            )
            return conn
        except mysql.connector.Error:
            retries -= 1
            time.sleep(2)
    raise Exception("Gagal terhubung ke database MySQL")

@app.route("/api/products/<int:id>")
def get_product(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products WHERE id = %s", (id,))
    product = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product)

@app.route("/api/products")
def list_products():
    category = request.args.get("category")
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if category:
        cursor.execute("SELECT * FROM products WHERE category = %s", (category,))
    else:
        cursor.execute("SELECT * FROM products")
        
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # Variasi 1: Output dinamis berdasarkan filter kategori
    if category:
        return jsonify({
            "category": category,
            "count": len(products),
            "products": products
        })
    return jsonify(products)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)