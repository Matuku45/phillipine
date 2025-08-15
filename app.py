import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # <-- Import CORS

app = Flask(__name__)
CORS(app)  # <-- Enable CORS for all domains. For production, restrict to your frontend URL.

# In-memory SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    agreed_to_terms = db.Column(db.Boolean, default=False)

# Create tables at startup
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    agreed_to_terms = data.get('agreed_to_terms', False)

    if not (name and email and password and agreed_to_terms):
        return jsonify({"error": "All fields required and terms must be agreed"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400

    new_user = User(name=name, email=email, password=password, agreed_to_terms=agreed_to_terms)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully", "user": {"name": name, "email": email}}), 201

@app.route('/users')
def get_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "name": u.name, "email": u.email, "agreed_to_terms": u.agreed_to_terms} for u in users])

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
