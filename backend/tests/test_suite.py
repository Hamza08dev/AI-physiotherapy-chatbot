import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import requests
import time
from concurrent.futures import ThreadPoolExecutor
import json
from app import app
from models.user import User, db

# Test configuration
BASE_URL = "http://localhost:5000"
TEST_USER = {
    "email": "test@example.com",
    "password": "testpassword123",
    "username": "testuser"
}

@pytest.fixture
def test_app():
    app.config['TESTING'] = True
    # Use environment variable for database URL if available, otherwise use SQLite
    database_url = os.getenv('DATABASE_URL', 'sqlite:///:memory:')
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(test_app):
    return test_app.test_client()

# Unit Tests
def test_user_model_creation(test_app):
    """Test user model creation and password hashing"""
    from flask_bcrypt import Bcrypt
    
    bcrypt = Bcrypt()
    with test_app.app_context():
        user = User(
            username="testuser",
            email="test@example.com",
            password_hash=bcrypt.generate_password_hash("testpassword123").decode('utf-8')
        )
        
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.password_hash is not None
        assert bcrypt.check_password_hash(user.password_hash, "testpassword123")

# Stress Tests
def test_stress_login(client):
    """Stress test for login endpoint"""
    # First create a test user
    signup_response = client.post(
        "/auth/signup",
        json=TEST_USER,
        headers={"Content-Type": "application/json"}
    )
    assert signup_response.status_code == 201

    num_requests = 100
    start_time = time.time()
    
    def make_login_request():
        try:
            response = client.post(
                "/auth/login",
                json={"email": TEST_USER["email"], "password": TEST_USER["password"]},
                headers={"Content-Type": "application/json"}
            )
            return response.status_code
        except Exception:
            return 500
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(lambda _: make_login_request(), range(num_requests)))
    
    end_time = time.time()
    total_time = end_time - start_time
    
    success_count = results.count(200)
    failure_count = len(results) - success_count
    
    print(f"\nStress Test Results:")
    print(f"Total Requests: {num_requests}")
    print(f"Successful Requests: {success_count}")
    print(f"Failed Requests: {failure_count}")
    print(f"Total Time: {total_time:.2f} seconds")
    print(f"Average Response Time: {(total_time/num_requests)*1000:.2f} ms")
    
    # Assert that all requests were successful
    assert success_count == num_requests, f"Expected {num_requests} successful requests, got {success_count}"
    assert failure_count == 0, f"Expected 0 failed requests, got {failure_count}"

# Regression Tests
def test_signup_login_flow(client):
    """Test the complete signup and login flow"""
    # Test signup
    signup_response = client.post(
        "/auth/signup",
        json=TEST_USER,
        headers={"Content-Type": "application/json"}
    )
    assert signup_response.status_code == 201
    assert b"token" in signup_response.data
    
    # Test login
    login_response = client.post(
        "/auth/login",
        json={"email": TEST_USER["email"], "password": TEST_USER["password"]},
        headers={"Content-Type": "application/json"}
    )
    assert login_response.status_code == 200
    assert b"token" in login_response.data

def test_invalid_login(client):
    """Test login with invalid credentials"""
    response = client.post(
        "/auth/login",
        json={"email": "wrong@example.com", "password": "wrongpass"},
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 401

if __name__ == "__main__":
    # Run unit tests and regression tests
    print("\nRunning pytest suite...")
    pytest.main(["-v", __file__])
    
    # Run stress test if the server is running
    try:
        requests.get(BASE_URL)
        print("\nServer is running. Starting stress test...")
        test_stress_login(client)
    except requests.exceptions.ConnectionError:
        print("\nCannot run stress test - server is not running")
        print("Please start the Flask server (python app.py) in a separate terminal") 