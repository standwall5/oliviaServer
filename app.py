from flask import Flask
from flask_cors import CORS
import os
from routes import login_route, signup_route, message_route, logout_route
from models import connect_db

app = Flask(__name__)

CORS(app, supports_credentials=True)

app.secret_key = os.urandom(24)
app.config.update(
    SESSION_COOKIE_SAMESITE='None',
    SESSION_COOKIE_SECURE=True  # Set this to True if using HTTPS
)

# Initialize database connection
connect_db(app)

# Register routes
app.register_blueprint(login_route)
app.register_blueprint(signup_route)
app.register_blueprint(message_route)
app.register_blueprint(logout_route)


if __name__ == '__main__':
    app.run(debug=True)