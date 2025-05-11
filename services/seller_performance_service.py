from data.db_connection import create_connection

def get_seller_performance():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.SellerName,
        AVG(l.CarPrice) AS avg_price,
        AVG(CASE WHEN l.AccidentsOrDamage ILIKE '%damage%' THEN 1 ELSE 0 END) AS damage_freq,
        AVG(l.Mileage) AS avg_mileage
        FROM Listings l
        JOIN Sellers s ON l.SellerID = s.SellerID
        GROUP BY s.SellerName
        ORDER BY avg_price DESC;
    """)
    result = cursor.fetchall()
    conn.close()
    return [
        {
            "seller_name": row[0],
            "avg_price": row[1],
            "damage_frequency": row[2],
            "avg_mileage": row[3]
        }
        for row in result
    ]
