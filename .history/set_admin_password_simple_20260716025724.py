import os
import pymysql
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv

load_dotenv()

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
        
        # Simple password
        new_password = "admin123"
        # Use werkzeug's password hashing (uses PBKDF2 which has no bcrypt issues)
        hashed = generate_password_hash(new_password)
        
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