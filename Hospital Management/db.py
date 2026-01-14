import pymysql

def get_connection():
    try:
        con = pymysql.connect(
            host="localhost",
            user="root",
            password="karthick",
            database="hospital_db"
        )
        return con
    except Exception as e:
        print("❌ Database connection failed:", e)
        return None
