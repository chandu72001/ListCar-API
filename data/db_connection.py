import psycopg2

def create_connection(db_name="vehicle_data"):
    """Creates and returns a connection to the given PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            host="localhost",
            dbname=db_name,
            user="postgres",
            password="123456"
        )
        print(f"Connected to database: {db_name}")
        return conn
    except Exception as e:
        print(f"Error connecting to {db_name}: {e}")
        return None
