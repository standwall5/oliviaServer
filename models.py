import psycopg2

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
        
        return user
    except Exception as e:
        print("Error: ", e)
        return None

def register_user(name, email, password):
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        
        # Query to insert the user into the database
        query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, email, password))
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