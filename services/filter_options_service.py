from data.db_connection import create_connection

def get_filter_options():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT FuelType FROM VehicleSpecs;")
    fuel_types = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT Drivetrain FROM VehicleSpecs;")
    drivetrains = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT ExteriorColor FROM Listings;")
    colors = [row[0] for row in cursor.fetchall()]

    conn.close()
    return {
        "fuel_types": fuel_types,
        "drivetrains": drivetrains,
        "colors": colors
    }
