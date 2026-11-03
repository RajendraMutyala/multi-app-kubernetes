
import os
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return "<h1>Payment Application</h1><p>Payment service is running.</p>"


@app.route("/payment")
def payment():
    return jsonify(
        application="payment",
        message="Payment Service is running!",
        status="success"
    )


@app.route("/health")
def health():
    return jsonify(status="healthy", application="payment"), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5001")))

