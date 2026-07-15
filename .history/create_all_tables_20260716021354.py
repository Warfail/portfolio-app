import os
import pymysql
from dotenv import load_dotenv
import ssl

load_dotenv()

def create_all_tables():
    print("🔧 Creating tables with secure connection...")
    print("=" * 60)
    
    try:
        # Secure connection with SSL
        connection = pymysql.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT')),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            ssl={'ssl-mode': 'REQUIRED'},
            connect_timeout=30
        )
        
        print("✅ Secure connection established!")
        
        with connection.cursor() as cursor:
            # Create profiles table
            print("📝 Creating profiles table...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS profiles (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(255) NOT NULL,
                    title VARCHAR(255) NOT NULL,
                    about TEXT NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    phone VARCHAR(50) NOT NULL,
                    location VARCHAR(255) NOT NULL,
                    linkedin VARCHAR(255),
                    github VARCHAR(255),
                    profile_image VARCHAR(500),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """)
            print("✅ profiles table created")
            
            # Create skills table
            print("📝 Creating skills table...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS skills (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    category VARCHAR(100) NOT NULL,
                    name VARCHAR(100) NOT NULL,
                    icon VARCHAR(100),
                    level INT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("✅ skills table created")
            
            # Create experiences table
            print("📝 Creating experiences table...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS experiences (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    company VARCHAR(255) NOT NULL,
                    position VARCHAR(255) NOT NULL,
                    location VARCHAR(255),
                    start_date DATETIME NOT NULL,
                    end_date DATETIME,
                    is_current BOOLEAN DEFAULT FALSE,
                    description TEXT,
                    achievements JSON,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """)
            print("✅ experiences table created")
            
            # Create projects table
            print("📝 Creating projects table...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    title VARCHAR(255) NOT NULL,
                    description TEXT NOT NULL,
                    technologies JSON,
                    image_url VARCHAR(500),
                    project_url VARCHAR(255),
                    github_url VARCHAR(255),
                    featured BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """)
            print("✅ projects table created")
            
            # Create contacts table
            print("📝 Creating contacts table...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    subject VARCHAR(255) NOT NULL,
                    message TEXT NOT NULL,
                    is_read BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("✅ contacts table created")
            
            # Create admins table
            print("📝 Creating admins table...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS admins (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    username VARCHAR(100) UNIQUE NOT NULL,
                    hashed_password VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("✅ admins table created")
            
            # Insert admin user
            print("📝 Inserting admin user...")
            cursor.execute("""
                INSERT IGNORE INTO admins (username, hashed_password) 
                VALUES ('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY3XhMKMhxTq5Ee')
            """)
            print("✅ Admin user inserted")
            
            # Insert profile
            print("📝 Inserting profile...")
            cursor.execute("""
                INSERT IGNORE INTO profiles (name, title, about, email, phone, location, linkedin, github) 
                VALUES (
                    'Rezky Agung Kurniawan',
                    'IT Infrastructure & Desktop Support Specialist',
                    'Hi, I''m Rezky Agung Kurniawan, an IT Infrastructure & Desktop Support Specialist passionate about building reliable, secure, and efficient IT environments.\n\nI have professional experience supporting enterprise infrastructure, managing Windows-based environments, deploying operating systems, administering Active Directory, monitoring network performance, and providing technical support for hundreds of end users. My background combines strong infrastructure knowledge with customer service experience, allowing me to communicate effectively while solving complex technical problems.\n\nCurrently, I work as an Infrastructure Support Specialist at Hejun Zongda Data Technology Co., Ltd., where I support enterprise infrastructure, manage Windows Server environments, deploy operating systems using Windows Deployment Services (WDS), administer Active Directory, monitor infrastructure with Zabbix, and manage incidents through ServiceNow.\n\nOutside of my professional work, I actively build software projects to sharpen my development skills, combining infrastructure expertise with modern web technologies and AI.',
                    'rezkytaewa2@gmail.com',
                    '+62 822-5967-0594',
                    'Sleman, Special Region of Yogyakarta, Indonesia',
                    'https://www.linkedin.com/in/rezkytaewa',
                    'https://github.com/Warfail'
                )
            """)
            print("✅ Profile inserted")
            
            # Insert skills (simplified version)
            print("📝 Inserting skills...")
            cursor.execute("""
                INSERT IGNORE INTO skills (category, name, level) VALUES
                ('Infrastructure & System Administration', 'Windows Server 2019', 85),
                ('Infrastructure & System Administration', 'Active Directory (AD)', 80),
                ('Networking', 'TCP/IP Networking', 75),
                ('Networking', 'DNS & DHCP', 70),
                ('Development', 'JavaScript', 65),
                ('Development', 'React', 60),
                ('Soft Skills', 'Analytical Problem Solving', 85),
                ('Soft Skills', 'Communication', 80)
            """)
            print("✅ Skills inserted")
            
            # Insert experiences
            print("📝 Inserting experiences...")
            cursor.execute("""
                INSERT IGNORE INTO experiences (company, position, location, start_date, end_date, is_current, description, achievements) VALUES
                (
                    'Hejun Zongda Data Technology Co., Ltd.',
                    'Infrastructure Support Specialist',
                    'Yogyakarta',
                    '2025-09-01 00:00:00',
                    NULL,
                    TRUE,
                    'Support infrastructure for approximately 350 enterprise workstations.',
                    '["Managed infrastructure for 350+ workstations", "Implemented WDS for OS deployment"]'
                ),
                (
                    'IGT Solutions',
                    'Customer Service Representative',
                    'Yogyakarta',
                    '2025-02-01 00:00:00',
                    '2025-09-01 00:00:00',
                    FALSE,
                    'Managed high-priority customer cases.',
                    '["Awarded Best Supportive Agent", "Managed high-priority cases"]'
                )
            """)
            print("✅ Experiences inserted")
            
            # Insert projects
            print("📝 Inserting projects...")
            cursor.execute("""
                INSERT IGNORE INTO projects (title, description, technologies, featured, project_url, github_url) VALUES
                (
                    'Restaurant POS System',
                    'A full-stack Point of Sale system for restaurants.',
                    '["React", "Node.js", "MongoDB"]',
                    TRUE,
                    NULL,
                    'https://github.com/Warfail'
                ),
                (
                    'AI Report Analyzer',
                    'AI-powered application that analyzes operational reports.',
                    '["Python", "FastAPI", "React"]',
                    TRUE,
                    NULL,
                    'https://github.com/Warfail'
                )
            """)
            print("✅ Projects inserted")
            
            connection.commit()
            print("=" * 60)
            print("✅ All tables and data created successfully!")
            
            # Verify
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"📋 Tables: {', '.join([t[0] for t in tables])}")
            
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    create_all_tables()