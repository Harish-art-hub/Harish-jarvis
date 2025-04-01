from flask import Flask, request, jsonify, redirect, url_for
from flask_cors import CORS
from database import db, cursor
import bcrypt

app = Flask(__name__)
CORS(app)  # Allow frontend requests

# ✅ Register API
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    # Hash password
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_pw))
        db.commit()
        return jsonify({"message": "User registered successfully!"}), 201
    except:
        return jsonify({"message": "Email already exists!"}), 400

# ✅ Login API (Standard Login)
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    cursor.execute("SELECT name, password FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()

    if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
        return jsonify({"success": True, "message": "Login successful!", "user": user[0]})
    else:
        return jsonify({"success": False, "message": "Invalid credentials!"}), 401

# ✅ J.A.R.V.I.S. Voice Login API
@app.route('/voice-login', methods=['POST'])
def voice_login():
    data = request.json
    email = data.get("email").strip().lower()
    password = data.get("password").strip()

    cursor.execute("SELECT name, password FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()

    if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
        return jsonify({"success": True, "message": "Voice Login successful!", "user": user[0]})
    else:
        return jsonify({"success": False, "message": "Voice Login failed!"}), 401

# ✅ Navigation API (For Voice Commands)
@app.route('/navigate/<page>', methods=['GET'])
def navigate(page):
    routes = {
        "home": "http://127.0.0.1:8000/home.html",
        "contact": "http://127.0.0.1:8000/contact.html",
        "about": "http://127.0.0.1:8000/about.html",
        "login": "http://127.0.0.1:8000/login.html"
    }

    if page in routes:
        return jsonify({"message": f"Redirecting to {page}", "url": routes[page]})
    else:
        return jsonify({"message": "Page not found"}), 404

# ✅ Logout API
@app.route('/logout', methods=['GET'])
def logout():
    return jsonify({"message": "User logged out successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
