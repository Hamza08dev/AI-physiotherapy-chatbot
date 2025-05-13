import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS  # ✅ Enable CORS for frontend communication
from dotenv import load_dotenv
from config import Config
from models.user import db
from routes.auth_routes import auth_bp
#from routes.chatbot_routes import chatbot_bp
from routes.chatbot_routes import chatbot_bp

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS for frontend requests
CORS(app, resources={r"/*": {"origins": "*"}})
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(chatbot_bp, url_prefix="/api/chatbot")
# Initialize database
db.init_app(app)

# Initialize JWT
jwt = JWTManager(app)

# Register Blueprints
#app.register_blueprint(chatbot_bp, url_prefix="/chatbot")

# Create database tables
with app.app_context():
    db.create_all()
    print("Database tables created successfully!")

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)
