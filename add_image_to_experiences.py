import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

def add_image_column():
    try:
        connection = pymysql.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT')),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            ssl={'ssl-mode': 'REQUIRED'}
        )
        
        with connection.cursor() as cursor:
            # Add image_url column to experiences table
            cursor.execute("""
                ALTER TABLE experiences 
                ADD COLUMN IF NOT EXISTS image_url VARCHAR(500)
            """)
            connection.commit()
            print("✅ Added image_url column to experiences table")
            
            # Verify
            cursor.execute("DESCRIBE experiences")
            columns = cursor.fetchall()
            print("\n📋 Columns in experiences:")
            for col in columns:
                print(f"  {col[0]} - {col[1]}")
        
        connection.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    add_image_column()