import pandas as pd
from db_connection import create_connection

def process_and_insert_data(df):
    """Process the data and insert into PostgreSQL."""
    conn = create_connection()
    if conn:
        cursor = conn.cursor()

        for _, row in df.iterrows():
            # Insert Seller Data
            cursor.execute("""
                INSERT INTO Sellers (SellerName, SellerRating, SellerAddress) 
                VALUES (%s, %s, %s) 
                RETURNING SellerID;
            """, (row['Seller Name'], row['Seller Rating'], row['Seller Address']))
            seller_id = cursor.fetchone()[0]

            # Insert VehicleSpecs Data
            cursor.execute("""
                INSERT INTO VehicleSpecs (VIN, CarName, Engine, FuelType, Transmission, Drivetrain, MPG)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (VIN) DO NOTHING;
            """, (row['VIN'], row['Car name'], row['Engine'], row['Fuel Type'], row['Transmission'], row['Drivetrain'], row['MPG']))

            # Insert Listings Data
            cursor.execute("""
                INSERT INTO Listings (VIN, CarPrice, CarPriceBadge, ExteriorColor, Mileage, AccidentsOrDamage, SellerID)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """, (row['VIN'], row['Car Price'], row['Car Price Badge'], row['Exterior Color'], row['Mileage'], row['Accidents or Damage'], seller_id))

        conn.commit()
        print("Data inserted successfully")
        conn.close()

# Example usage
if __name__ == "__main__":
    # Load the cleaned data
    df = pd.read_csv('data/processed/vehicle_data_cleaned.csv')  # Load the cleaned data
    process_and_insert_data(df)