from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from models.user import User, db
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token

import traceback  # ✅ Import for debugging

bcrypt = Bcrypt()
auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["POST"])
@cross_origin(origins="*")  # ✅ Allow CORS for this route
def signup():
    try:
        print("Signup route hit!")
        data = request.json
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        print(f"Received Signup Request: {data}")

        if not username or not email or not password:
            return jsonify({"message": "All fields are required"}), 400

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"message": "Email already exists"}), 400

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        new_user = User(username=username, email=email, password_hash=hashed_password)  # ✅ Updated field name

        db.session.add(new_user)
        db.session.commit()

        access_token = create_access_token(identity={"email": email})

        return jsonify({"message": "User created successfully", "token": access_token}), 201
    except Exception as e:
        print(f"Signup Error: {str(e)}")
        traceback.print_exc()
        return jsonify({"error": "Internal Server Error"}), 500
    

    # ✅ NEW LOGIN ROUTE
@auth_bp.route("/login", methods=["POST"])
@cross_origin(origins="http://localhost:3000")
def login():
    try:
        data = request.json
        email = data.get("email")
        password = data.get("password")

        print(f"Received Login Request: {data}")

        if not email or not password:
            return jsonify({"message": "Email and password are required"}), 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"message": "Invalid email or password"}), 401

        if not bcrypt.check_password_hash(user.password_hash, password):
            return jsonify({"message": "Invalid email or password"}), 401

        access_token = create_access_token(identity={"email": user.email})
        return jsonify({"message": "Login successful", "token": access_token}), 200
    except Exception as e:
        print(f"Login Error: {str(e)}")
        traceback.print_exc()
        return jsonify({"error": "Internal Server Error"}), 500
