import psycopg2
import bcrypt

DB_HOST = "dpg-ctgh6ergbbvc738q4gh0-a.singapore-postgres.render.com"
DB_NAME = "oliviadb_3q1f"
DB_USER = "olivia"
DB_PASSWORD = "UQOeX7M9u6BNtKWbfhQ4kUl5txdCQ1gt"

def connect_db(app):
    app.config['DB_HOST'] = DB_HOST
    app.config['DB_NAME'] = DB_NAME
    app.config['DB_USER'] = DB_USER
    app.config['DB_PASSWORD'] = DB_PASSWORD

def validate_user(email, password):
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        
        # Fetch the user record based on the email (do not check password here)
        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()
        conn.close()

        if user:
            # Assuming the password is in the 3rd column (index 2)
            stored_password = user[3]  # Index 2 is for the password column in the table

            # Check if the entered password matches the hashed password stored in the database
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                return user  # Return the whole user record, including the id
            else:
                return None  # Invalid password
        else:
            return None  # Invalid email

    except Exception as e:
        print("Error: ", e)
        return None

def register_user(name, email, password):
    try:
        # Hash the password before saving it to the database
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        
        #Check if user exists, return false
        query = "SELECT email FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        userExists = cursor.fetchone()

        if userExists:
            return 'exists'
        else:

            # Query to insert the user into the database
            query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, email, hashed_password.decode('utf-8')))  # Store the hashed password as string
            conn.commit()
            
            conn.close()
            
            return True
    except Exception as e:
        print("Error: ", e)
        return False
    
def add_message(id, username, content):
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()

        query = "INSERT INTO messages (user_id, username, message) VALUES (%s, %s, %s)"
        cursor.execute(query, (id, username, content))
        conn.commit()

        conn.close()

        return True
    except Exception as e:
        print("Error: ", e)
        return False
    
def get_messages():
    try:
        
    # # Get query parameters for pagination
        # page = int(request.args.get('page', 1))  # Default to page 1
        # per_page = int(request.args.get('per_page', 10))  # Default to 10 messages per page
        # offset = (page - 1) * per_page

        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()

        # Fetch messages with pagination
        query = """
        SELECT username, message
        FROM messages
        ORDER BY id DESC
        LIMIT 10
        """
        cursor.execute(query)
        messages = cursor.fetchall()
        conn.close()

        return messages
    except Exception as e:
        print("Error: ", e)
        return None
        

