Let's first create the four application scripts for your CI/CD project: Frontend, Login, Payment, and Product. We'll use Python Flask because it is lightweight and easy to containerize with Docker.

These applications will communicate with each other through Kubernetes Services. Later, GitHub Actions will build and deploy them automatically.
1. Project folder structure
Create this structure on your Mac:
multi-app-kubernetes/
├── frontend/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── login/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── payment/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
└── product/
    ├── app.py
    ├── requirements.txt
    └── Dockerfile


Run:
mkdir -p multi-app-kubernetes/{frontend,login,payment,product}
cd multi-app-kubernetes


2. Frontend application
This is the main website users visit. It displays links to the Login, Payment, and Product services and calls the other applications through their Kubernetes Service names.

File: frontend/app.py

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




3. Login application
File: login/app.py

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




This is a demonstration endpoint only. It does not authenticate real users or store passwords.
4. Payment application
File: payment/app.py

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




This is a mock payment service; it does not process actual payments or card information.
5. Product application
File: product/app.py

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




6. Add the Python dependencies
Create a requirements.txt inside each of the four application folders. Use the following content in all four files:
Flask>=3.1,<4.0
requests>=2.32,<3.0


The frontend needs requests to call the other services. The other three applications don't use it yet, but including it in all four keeps the initial setup simple.
7. Add a Dockerfile for each application
Create a file named Dockerfile inside each application folder.

Use this Dockerfile for the frontend:

frontend/Dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8000

CMD ["python", "app.py"]


For login/Dockerfile, use the same content but change:
EXPOSE 5000


For payment/Dockerfile, change it to:
EXPOSE 5001


For product/Dockerfile, change it to:
EXPOSE 5002


Keep all the other Dockerfile lines unchanged.
8. Test an application locally
Start with the Login application:
cd login

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
python app.py


Open another terminal and test it:
curl http://localhost:5000/login
curl http://localhost:5000/health


You should receive JSON responses showing that the Login service is running.

Repeat the same process for the other applications, using their respective ports.
9. What happens when you change the code?
For example, change the welcome message in frontend/app.py, then push the change to GitHub.

The CI/CD pipeline we'll create next will:
1. Detect the push to GitHub.
2. Build the updated Docker images.
3. Push the images to GHCR or Docker Hub.
4. Update the corresponding Kubernetes Deployments.
5. Wait for the new Pods to become ready.
Important: These scripts are the application layer only. They don't deploy themselves to Kubernetes yet. The next step is to create the Kubernetes YAML files for all four apps, including their Deployments, Services, ports and frontend environment variables.
