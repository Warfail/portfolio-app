import os
import sys
from pathlib import Path
import pymysql
from dotenv import load_dotenv

# Get the project root directory
project_root = Path(__file__).parent

# Try to load .env from different locations
env_paths = [
    project_root / '.env',
    project_root / 'backend' / '.env',
    project_root / '.env.example'
]

print("🔍 Looking for .env file...")
for path in env_paths:
    if path.exists():
        print(f"✅ Found .env at: {path}")
        load_dotenv(path)
        break
else:
    print("❌ No .env file found!")
    print(f"📁 Please create .env in: {project_root / '.env'}")
    sys.exit(1)

print("=" * 60)

# Get credentials
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
database = os.getenv('DB_NAME')

print(f"📌 DB_HOST: {host}")
print(f"📌 DB_PORT: {port}")
print(f"📌 DB_USER: {user}")
print(f"📌 DB_NAME: {database}")
print("=" * 60)

if not all([host, user, password, database]):
    print("❌ Missing environment variables! Check your .env file")
    print("\nExpected variables:")
    print("  DB_HOST=gateway01.ap-southeast-1.prod.aws.tidbcloud.com")
    print("  DB_PORT=4000")
    print("  DB_USER=4Ybh3MVBCYQ2ox2.root")
    print("  DB_PASSWORD=Vuy0Q3xud4EUpkJH")
    print("  DB_NAME=portfolio_db")
    sys.exit(1)

try:
    print("🔌 Attempting to connect to TiDB Cloud...")
    connection = pymysql.connect(
        host=host,
        port=int(port),
        user=user,
        password=password,
        database=database,
        connect_timeout=30,
        ssl={'ca': None}  # TiDB Cloud requires SSL
    )
    
    print("✅ Connection successful!")
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"📊 TiDB Version: {version[0]}")
        
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        if tables:
            print(f"📋 Tables found: {', '.join([t[0] for t in tables])}")
        else:
            print("📋 No tables found yet.")
    
    connection.close()
    
except pymysql.err.OperationalError as e:
    print(f"❌ Connection failed: {e}")
    print("\n💡 Troubleshooting tips:")
    print("1. Make sure your IP is whitelisted in TiDB Cloud")
    print("2. Check the database name: portfolio_db")
    print("3. Verify your password")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()