from data.db_connection import create_connection
import math

def get_fuel_efficiency(fuel_type=None):
    def label_efficiency(avg_mpg):
        if avg_mpg is None or not math.isfinite(avg_mpg):
            return "Unknown"
        elif avg_mpg >= 30:
            return "Efficient"
        elif avg_mpg >= 20:
            return "Moderate"
        else:
            return "Poor"

    conn = create_connection()
    cursor = conn.cursor()

    if fuel_type:
        cursor.execute("""
            SELECT CarName, AVG(CAST(MPG AS FLOAT))
            FROM VehicleSpecs
            WHERE FuelType = %s AND MPG IS NOT NULL AND MPG != 'NaN'
            GROUP BY CarName
            ORDER BY AVG(MPG) DESC
        """, (fuel_type,))
    else:
        cursor.execute("""
            SELECT CarName, AVG(CAST(MPG AS FLOAT))
            FROM VehicleSpecs
            WHERE MPG IS NOT NULL AND MPG != 'NaN' AND CarName IS NOT NULL
            GROUP BY CarName
            ORDER BY AVG(MPG) DESC
        """)

    result = cursor.fetchall()
    conn.close()

    return [
        {
            "car_name": row[0],
            "avg_mpg": round(row[1], 2) if row[1] and math.isfinite(row[1]) else None,
            "efficiency_label": label_efficiency(row[1])
        }
        for row in result
    ]