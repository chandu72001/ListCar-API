from data.db_connection import create_connection

def get_damage_impact():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT vs.CarName,
            AVG(CASE WHEN l.AccidentsOrDamage ILIKE '%damage%' THEN l.CarPrice ELSE NULL END) AS damaged_price,
            AVG(CASE WHEN l.AccidentsOrDamage IS NULL OR l.AccidentsOrDamage ILIKE 'no%' THEN l.CarPrice ELSE NULL END) AS undamaged_price
        FROM Listings l
        JOIN VehicleSpecs vs ON l.VIN = vs.VIN
        GROUP BY vs.CarName;
    """)
    result = cursor.fetchall()
    conn.close()
    return [
        {
            "car_name": row[0],
            "avg_damaged_price": row[1],
            "avg_undamaged_price": row[2],
            "price_difference": (row[2] or 0) - (row[1] or 0)
        }
        for row in result
    ]
