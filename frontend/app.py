
import os
from flask import Flask, jsonify
import requests

app = Flask(__name__)

LOGIN_URL = os.getenv("LOGIN_URL", "http://localhost:5000")
PAYMENT_URL = os.getenv("PAYMENT_URL", "http://localhost:5001")
PRODUCT_URL = os.getenv("PRODUCT_URL", "http://localhost:5002")


@app.route("/")
def home():
    return """
    <html>
      <head><title>Multi-App Website</title></head>
      <body>
        <h1>Hi, from my CI/CD kubernetes Project - Version 4!</h1>
        <h1>Welcome to My Multi-App Website</h1>
        <p>Deployed with Docker, Kubernetes and GitHub Actions.</p>
        <ul>
          <li><a href="/login">Login Service</a></li>
          <li><a href="/payment">Payment Service</a></li>
          <li><a href="/products">Product Service</a></li>
        </ul>
      </body>
    </html>
    """


@app.route("/login")
def login():
    try:
        response = requests.get(f"{LOGIN_URL}/login", timeout=3)
        return response.text, response.status_code
    except requests.RequestException as error:
        return jsonify(error="Login service unavailable", detail=str(error)), 503


@app.route("/payment")
def payment():
    try:
        response = requests.get(f"{PAYMENT_URL}/payment", timeout=3)
        return response.text, response.status_code
    except requests.RequestException as error:
        return jsonify(error="Payment service unavailable", detail=str(error)), 503


@app.route("/products")
def products():
    try:
        response = requests.get(f"{PRODUCT_URL}/products", timeout=3)
        return response.text, response.status_code
    except requests.RequestException as error:
        return jsonify(error="Product service unavailable", detail=str(error)), 503


@app.route("/health")
def health():
    return jsonify(status="healthy", application="frontend"), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")))

