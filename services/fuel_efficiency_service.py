from data.db_connection import create_connection

def get_fuel_efficiency(fuel_type=None):
    conn = create_connection()
    cursor = conn.cursor()
    if fuel_type:
        cursor.execute("""
            SELECT CarName, AVG(MPG)
            FROM VehicleSpecs
            WHERE FuelType = %s
            GROUP BY CarName
            ORDER BY AVG(MPG) DESC
        """, (fuel_type,))
    else:
        cursor.execute("""
            SELECT FuelType, AVG(MPG)
            FROM VehicleSpecs
            GROUP BY FuelType
            ORDER BY AVG(MPG) DESC
        """)
    result = cursor.fetchall()
    conn.close()
    return [{"label": row[0], "avg_mpg": row[1]} for row in result]
