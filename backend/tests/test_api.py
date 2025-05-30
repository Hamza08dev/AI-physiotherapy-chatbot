import os
import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from routes.auth_routes import auth_bp  # Updated import path

# Initialize SQLAlchemy and Flask app
db = SQLAlchemy()

@pytest.fixture
def app():
    # Set up the Flask application for testing
    app = Flask(__name__)
    # Use environment variable for database URL if available, otherwise use SQLite
    database_url = os.getenv('DATABASE_URL', 'sqlite:///:memory:')
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key')
    
    db.init_app(app)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    # Create the database tables
    with app.app_context():
        db.create_all()
    
    yield app  # This provides the app to the test case
    
    # Cleanup after the test case
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_signup(client):
    response = client.post('/auth/signup', json={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'securepassword123'
    })
    
    # Assert response status code is 201 (Created)
    assert response.status_code == 201
    assert 'token' in response.json  # Ensure the response includes a token
