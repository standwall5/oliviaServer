from flask import Flask
from flask_cors import CORS
from routes import login_route, signup_route, message_route
from models import connect_db

app = Flask(__name__)

CORS(app)

# Initialize database connection
connect_db(app)

# Register routes
app.register_blueprint(login_route)
app.register_blueprint(signup_route)
app.register_blueprint(message_route)

if __name__ == '__main__':
    app.run(debug=True)