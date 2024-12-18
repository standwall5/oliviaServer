from flask import Flask, request, jsonify
import psycopg2
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

# Database connection details
DB_HOST = "dpg-ctgh6ergbbvc738q4gh0-a.singapore-postgres.render.com"
DB_NAME = "oliviadb_3q1f"
DB_USER = "olivia"
DB_PASSWORD = "UQOeX7M9u6BNtKWbfhQ4kUl5txdCQ1gt"

# Route to handle login
@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return jsonify({"status": "error", "message": "Email and password are required."}), 400

    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()

        # Query to check user credentials
        query = "SELECT * FROM users WHERE email = %s AND password = %s"
        cursor.execute(query, (email, password))
        user = cursor.fetchone()

        if user:
            return jsonify({"status": "success", "message": "Login successful!"})
        else:
            return jsonify({"status": "error", "message": "Invalid email or password."}), 401

    except Exception as e:
        return jsonify({"status": "error", "message": "An error occurred.", "details": str(e)}), 500

    finally:
        if conn:
            cursor.close()
            conn.close()

# Start the Flask server
if __name__ == '__main__':
    app.run(debug=True)
