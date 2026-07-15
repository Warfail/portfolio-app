import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

def test_tidb_connection():
    print("🔍 Testing TiDB Connection...")
    print("=" * 50)
    
    # Get credentials from .env
    host = os.getenv('DB_HOST')
    port = int(os.getenv('DB_PORT', 4000))
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    database = os.getenv('DB_NAME')
    
    print(f"📌 Host: {host}")
    print(f"📌 Port: {port}")
    print(f"📌 User: {user}")
    print(f"📌 Database: {database}")
    print("=" * 50)
    
    try:
        # Try to connect
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            connect_timeout=10
        )
        
        print("✅ Connection successful!")
        
        # Test query
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"📊 TiDB Version: {version[0]}")
            
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            if tables:
                print(f"📋 Tables found: {', '.join([t[0] for t in tables])}")
            else:
                print("📋 No tables found. You need to create them.")
        
        connection.close()
        return True
        
    except pymysql.err.OperationalError as e:
        print(f"❌ Connection failed: {e}")
        print("\n💡 Troubleshooting tips:")
        print("1. Make sure your IP is whitelisted in TiDB Cloud")
        print("2. Check if the database name is correct")
        print("3. Verify your username and password")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_tidb_connection()