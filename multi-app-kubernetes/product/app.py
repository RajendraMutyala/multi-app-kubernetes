
import os
from flask import Flask, jsonify

app = Flask(__name__)

PRODUCTS = [
    {"id": 1, "name": "Laptop", "price": 65000},
    {"id": 2, "name": "Mobile Phone", "price": 25000},
    {"id": 3, "name": "Headphones", "price": 3000}
]


@app.route("/")
def home():
    return "<h1>Product Application</h1><p>Product service is running.</p>"


@app.route("/products")
def products():
    return jsonify(
        application="product",
        products=PRODUCTS,
        status="success"
    )


@app.route("/health")
def health():
    return jsonify(status="healthy", application="product"), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5002")))

