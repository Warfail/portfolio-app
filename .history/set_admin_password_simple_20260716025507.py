import os
import pymysql
from passlib.context import CryptContext
from dotenv import load_dotenv

load_dotenv()

# Use bcrypt with simple settings
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def set_admin_password():
    try:
        connection = pymysql.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT')),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            ssl={'ssl-mode': 'REQUIRED'}
        )
        
        # Short and simple password
        new_password = "admin123"
        hashed = pwd_context.hash(new_password)
        
        with connection.cursor() as cursor:
            # Update admin password
            cursor.execute(
                "UPDATE admins SET hashed_password = %s WHERE username = 'admin'",
                (hashed,)
            )
            connection.commit()
            
            # Check if updated
            cursor.execute("SELECT username FROM admins WHERE username = 'admin'")
            result = cursor.fetchone()
            
            if result:
                print(f"✅ Admin password updated successfully!")
                print(f"   Username: admin")
                print(f"   Password: {new_password}")
            else:
                # Create admin if doesn't exist
                cursor.execute(
                    "INSERT INTO admins (username, hashed_password) VALUES (%s, %s)",
                    ("admin", hashed)
                )
                connection.commit()
                print(f"✅ Admin created successfully!")
                print(f"   Username: admin")
                print(f"   Password: {new_password}")
        
        connection.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    set_admin_password()