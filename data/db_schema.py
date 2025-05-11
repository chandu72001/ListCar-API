import logging
import psycopg2
from db_connection import create_connection

# Setting up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def create_database():
    """Creates the 'vehicle_data' database if it doesn't exist."""
    try:
        conn = psycopg2.connect(
            host="localhost",
            dbname="postgres",
            user="postgres",
            password="123456"
        )
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'vehicle_data'")
        exists = cursor.fetchone()

        if not exists:
            cursor.execute("CREATE DATABASE vehicle_data")
            logger.info("Database 'vehicle_data' created.")
        else:
            logger.info("Database 'vehicle_data' already exists.")

        cursor.close()
        conn.close()
    except Exception as e:
        logger.error(f"Error creating database: {e}")

def create_tables():
    """Creates the necessary tables inside the 'vehicle_data' database."""
    conn = create_connection("vehicle_data")
    if conn:
        try:
            cursor = conn.cursor()

            # Sellers Table
            cursor.execute(""" 
                CREATE TABLE IF NOT EXISTS Sellers (
                    SellerID SERIAL PRIMARY KEY,
                    SellerName VARCHAR(255),
                    SellerRating FLOAT,
                    SellerAddress VARCHAR(255)
                );
            """)

            # VehicleSpecs Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS VehicleSpecs (
                    VIN VARCHAR(20) PRIMARY KEY,
                    CarName VARCHAR(255),
                    Engine VARCHAR(255),
                    FuelType VARCHAR(50),
                    Transmission VARCHAR(50),
                    Drivetrain VARCHAR(50),
                    MPG FLOAT
                );
            """)

            # Listings Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Listings (
                    ListingID SERIAL PRIMARY KEY,
                    VIN VARCHAR(20) REFERENCES VehicleSpecs(VIN),
                    CarPrice FLOAT,
                    CarPriceBadge VARCHAR(100),
                    ExteriorColor VARCHAR(50),
                    Mileage INTEGER,
                    AccidentsOrDamage VARCHAR(100),
                    SellerID INTEGER REFERENCES Sellers(SellerID)
                );
            """)

            conn.commit()
            logger.info("All tables created successfully.")
        except Exception as e:
            logger.error(f"Error creating tables: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    create_database()
    create_tables()