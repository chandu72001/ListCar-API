from data.db_connection import create_connection

def get_top_models():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT vs.CarName, COUNT(*) AS listing_count, MAX(l.CarPrice) AS max_price
        FROM Listings l
        JOIN VehicleSpecs vs ON l.VIN = vs.VIN
        GROUP BY vs.CarName
        ORDER BY listing_count DESC, max_price DESC
        LIMIT 10;
    """)
    result = cursor.fetchall()
    conn.close()
    return [{"car_name": row[0], "listing_count": row[1], "max_price": row[2]} for row in result]