
import os
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return "<h1>Login Application</h1><p>Login service is running.</p>"


@app.route("/login")
def login():
    return jsonify(
        application="login",
        message="Welcome to the Login Service!",
        status="success"
    )


@app.route("/health")
def health():
    return jsonify(status="healthy", application="login"), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))

