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
        query = "SELECT * FROM users WHERE email = %s AND password = %s"
        cursor.execute(query, (email, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            # Assuming the password is in the 3rd column (index 2)
            stored_password = user[2]  # Index 2 is for the password column in the table

            # Check if the password entered matches the hashed password in the database
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
        
        # Query to insert the user into the database
        query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, email, hashed_password.decode('utf-8')))  # Store the hashed password as string
        conn.commit()
        
        conn.close()
        
        return True
    except Exception as e:
        print("Error: ", e)
        return False
    
def message(id, username, content):
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