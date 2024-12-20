from flask import Blueprint, request, jsonify, session
from models import validate_user, register_user, add_message, get_messages

login_route = Blueprint('login', __name__)
signup_route = Blueprint('signup', __name__)
message_route = Blueprint('message', __name__)
logout_route = Blueprint('logout',__name__)

# Login Route
@login_route.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return jsonify({"status": "error", "message": "Email and password are required."}), 400

    user = validate_user(email, password)

    if user:
        session['user_id'] = user[0] # user[0] is the index of the 'id' field in the database
        print("Session ID: ", session.get('user_id'))
        return jsonify({"status": "success", "message": "Login successful!"})
    else:
        return jsonify({"status": "error", "message": "Invalid email or password."}), 401

# Signup Route
@signup_route.route('/signup', methods=['POST'])
def signup():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    
    if not email or not password:
        return jsonify({"status": "error", "message": "Please make sure all fields are complete."}), 400

    # You can add more validation here, like checking if the user already exists
    success = register_user(name, email, password)

    if success == 'exists':
        return jsonify({"status": "error", "message": "Account already exists."}), 409
    elif success == True:
        return jsonify({"status": "success", "message": "Signup successful!"})
    else:
        return jsonify({"status": "error", "message": "Failed to sign up. Try again."}), 500

# Message Route
@message_route.route('/message', methods=['POST'])
def send_message():

    id = session.get('user_id')

    if not id:
        return jsonify({"status": "error", "message": "User not logged in."}), 401
    
    username = request.form.get('username')
    content = request.form.get('content')

    if not username or not content:
        return jsonify({"status": "success", "message": "Name or message cannot be empty. Please try again."}), 400
    
    sent = add_message(id, username, content)

    if sent:
        return jsonify({"status": "success", "message": "Message sent to Olivia!"})
    else:
        return jsonify({"status": "error", "message": "Failed to send message. Try again."}), 500

@message_route.route('/getmessages', methods=['GET'])
def display_messages():
    try:
        messages = get_messages()

        if not messages:  # If no messages found or error occurred
            return jsonify({"status": "error", "message": "Failed to fetch messages."}), 500

        formatted_messages = [{"username": msg[0], "message": msg[1]} for msg in messages]
        return jsonify({"status": "success", "data": formatted_messages})
    
    except Exception as e:
        print("Error: ", e)
        return jsonify({"status": "error", "message": "Failed to fetch messages."}), 500

# Logout Route
@logout_route.route('/logout', methods=['POST'])
def logout():
    # Clear the session
    session.clear()

    return jsonify({"status": "success", "message": "You have been logged out."})