import os
import pymysql
import json
from dotenv import load_dotenv

load_dotenv()

def reseed_portfolio():
    print("🔄 Reseeding complete portfolio data...")
    print("=" * 60)
    
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
            # ==========================================
            # 1. CLEAR ALL EXISTING DATA
            # ==========================================
            print("\n🗑️  Clearing existing data...")
            cursor.execute("DELETE FROM projects")
            cursor.execute("DELETE FROM experiences")
            cursor.execute("DELETE FROM skills")
            cursor.execute("DELETE FROM profiles")
            cursor.execute("DELETE FROM contacts")
            print("✅ All data cleared")
            
            # ==========================================
            # 2. PROFILE
            # ==========================================
            print("\n📝 Seeding profile...")
            cursor.execute("""
                INSERT INTO profiles (name, title, about, email, phone, location, linkedin, github) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                "Rezky Agung Kurniawan",
                "IT Infrastructure Engineer",
                """Hi, I'm Rezky Agung Kurniawan, an IT Infrastructure Engineer with hands-on experience in enterprise infrastructure, system administration, desktop support, and full-stack web development.

Over the past several years, I've worked in IT vendor companies, international BPO environments, and enterprise infrastructure teams, supporting over 1,500 IT assets across multiple organizations. My experience ranges from Windows Server administration, Active Directory, Windows Deployment Services (WDS), infrastructure monitoring with Zabbix, ServiceNow incident management, enterprise desktop support, and basic Huawei network configuration.

Alongside my infrastructure career, I actively develop modern web applications and AI-powered solutions. I enjoy combining infrastructure knowledge with software engineering to build systems that are reliable, scalable, and user-friendly.

My goal is to continue growing as an Infrastructure Engineer while expanding into DevOps, Cloud Infrastructure, and automation technologies.""",
                "rezkytaewa2@gmail.com",
                "+62 822-5967-0594",
                "Sleman, Special Region of Yogyakarta, Indonesia",
                "https://www.linkedin.com/in/rezkytaewa",
                "https://github.com/Warfail"
            ))
            print("✅ Profile seeded")

            # ==========================================
            # 3. EXPERIENCES
            # ==========================================
            print("\n📝 Seeding experiences...")
            
            experiences = [
                {
                    "company": "Hejun Zongda Data Technology Co., Ltd.",
                    "position": "Infrastructure Support Specialist",
                    "location": "Yogyakarta, Indonesia",
                    "start_date": "2025-09-01",
                    "end_date": None,
                    "is_current": 1,
                    "description": "Support enterprise infrastructure for approximately 350 workstations. Administer Windows Server 2019 environments. Deploy operating systems using Windows Deployment Services (WDS). Manage Active Directory users, permissions, and Group Policies. Monitor infrastructure availability using Zabbix. Handle incidents and service requests using ServiceNow (SNOW). Perform asset lifecycle management and infrastructure troubleshooting.",
                    "achievements": [
                        "Support infrastructure for 350+ workstations",
                        "Administer Windows Server 2019",
                        "Deploy OS via WDS",
                        "Manage Active Directory & Group Policies",
                        "Monitor infrastructure with Zabbix",
                        "Handle incidents via ServiceNow"
                    ]
                },
                {
                    "company": "IGT Solutions",
                    "position": "Customer Service Representative",
                    "location": "Yogyakarta, Indonesia",
                    "start_date": "2025-02-01",
                    "end_date": "2025-09-01",
                    "is_current": 0,
                    "description": "Managed complex customer support cases. Maintained SLA and compliance standards. Received the Best Supportive Agent award for reliability and teamwork.",
                    "achievements": [
                        "Managed complex customer support cases",
                        "Maintained SLA and compliance standards",
                        "Received Best Supportive Agent award"
                    ]
                },
                {
                    "company": "Teleperformance",
                    "position": "Infrastructure Desktop Support",
                    "location": "Jakarta, Indonesia",
                    "start_date": "2024-05-01",
                    "end_date": "2024-12-01",
                    "is_current": 0,
                    "description": "Delivered internal infrastructure and desktop support. Resolved hardware, software, and network-related issues. Assisted users with workstation deployment and maintenance.",
                    "achievements": [
                        "Delivered internal infrastructure and desktop support",
                        "Resolved hardware, software, and network issues",
                        "Assisted with workstation deployment and maintenance"
                    ]
                },
                {
                    "company": "Bursa Multimedia Group",
                    "position": "IT Technical Support",
                    "location": "Yogyakarta, Indonesia",
                    "start_date": "2022-07-01",
                    "end_date": "2024-03-01",
                    "is_current": 0,
                    "description": "An IT vendor company providing infrastructure services for multiple BPO organizations. Managed and maintained approximately 1,500 IT assets. Performed hardware, software, and network troubleshooting. Supported desktop deployment and infrastructure maintenance. Worked as an on-site IT support engineer for multiple enterprise clients. Maintained asset inventory and device lifecycle records. Delivered technical support while meeting client SLA requirements.",
                    "achievements": [
                        "Managed 1,500+ IT assets",
                        "Performed hardware, software, and network troubleshooting",
                        "Supported desktop deployment and infrastructure maintenance",
                        "Worked as on-site IT support engineer",
                        "Maintained asset inventory and device lifecycle records",
                        "Delivered technical support meeting SLA requirements"
                    ]
                }
            ]
            
            for exp in experiences:
                cursor.execute("""
                    INSERT INTO experiences 
                    (company, position, location, start_date, end_date, is_current, description, achievements) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    exp["company"],
                    exp["position"],
                    exp["location"],
                    exp["start_date"],
                    exp["end_date"],
                    exp["is_current"],
                    exp["description"],
                    json.dumps(exp["achievements"])
                ))
                print(f"  ✅ {exp['position']} at {exp['company']}")

            # ==========================================
            # 4. SKILLS
            # ==========================================
            print("\n📝 Seeding skills...")
            
            skills = [
                # Infrastructure
                ("Infrastructure", "Windows Server 2019", 85),
                ("Infrastructure", "Active Directory", 80),
                ("Infrastructure", "Group Policy (GPO)", 75),
                ("Infrastructure", "Windows Deployment Services (WDS)", 70),
                ("Infrastructure", "Windows Administration", 85),
                ("Infrastructure", "Desktop Support", 85),
                ("Infrastructure", "IT Asset Management", 80),
                # Networking
                ("Networking", "TCP/IP", 75),
                ("Networking", "DNS & DHCP", 70),
                ("Networking", "Basic Huawei Switch Configuration", 60),
                ("Networking", "Network Troubleshooting", 80),
                ("Networking", "Infrastructure Monitoring (Zabbix)", 70),
                # Virtualization
                ("Virtualization", "Oracle VM VirtualBox", 70),
                # IT Operations
                ("IT Operations", "ServiceNow (SNOW)", 75),
                ("IT Operations", "Incident Management", 80),
                ("IT Operations", "Change Management", 70),
                ("IT Operations", "Asset Lifecycle Management", 75),
                ("IT Operations", "End-user Support", 85),
                # Development
                ("Development", "React", 60),
                ("Development", "JavaScript", 65),
                ("Development", "Node.js", 60),
                ("Development", "MongoDB", 55),
                ("Development", "REST API", 65),
                ("Development", "Git & GitHub", 70)
            ]
            
            for category, name, level in skills:
                cursor.execute(
                    "INSERT INTO skills (category, name, level) VALUES (%s, %s, %s)",
                    (category, name, level)
                )
            print(f"  ✅ {len(skills)} skills seeded")

            # ==========================================
            # 5. PROJECTS
            # ==========================================
            print("\n📝 Seeding projects...")
            
            projects = [
                {
                    "title": "Restaurant POS System",
                    "description": "A modern restaurant Point of Sale application supporting cashier operations, QR table ordering, kitchen workflow, menu management, and sales reporting.",
                    "technologies": json.dumps(["React", "Node.js", "MongoDB", "REST API", "Vite"]),
                    "project_url": "https://restoran-frontend-nu.vercel.app",
                    "github_url": "https://github.com/Warfail/restoran-frontend",
                    "featured": 1
                },
                {
                    "title": "AI Report Analyzer",
                    "description": "An AI-powered application that analyzes operational reports and automatically determines urgency levels for each department to improve incident prioritization.",
                    "technologies": json.dumps(["Python", "FastAPI", "HTML/CSS", "JavaScript", "AI/ML", "Generative AI"]),
                    "project_url": "",
                    "github_url": "https://github.com/Warfail/free-report-analyzer",
                    "featured": 1
                },
                {
                    "title": "Bursa Sewa Laptop - Company Landing Page",
                    "description": "Designed and developed the official company landing page to improve online presence, showcase services, and provide a modern, responsive user experience.",
                    "technologies": json.dumps(["HTML", "CSS", "JavaScript", "Bootstrap"]),
                    "project_url": "https://bursasewalaptop.github.io",
                    "github_url": "",
                    "featured": 0
                }
            ]
            
            for project in projects:
                cursor.execute("""
                    INSERT INTO projects 
                    (title, description, technologies, project_url, github_url, featured) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    project["title"],
                    project["description"],
                    project["technologies"],
                    project["project_url"],
                    project["github_url"],
                    project["featured"]
                ))
                print(f"  ✅ {project['title']}")

            # ==========================================
            # 6. ADMIN (Keep existing or create new)
            # ==========================================
            print("\n📝 Ensuring admin exists...")
            cursor.execute("SELECT id FROM admins WHERE username = 'admin'")
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO admins (username, hashed_password) 
                    VALUES ('admin', 'pbkdf2:sha256:260000$S49VNXzWeCwYfEza$20851cdd23951c91a8108ab36b3c25a058f901ded94b30b7114d5f1bb8d4b3c3')
                """)
                print("  ✅ Admin created (password: admin123)")
            else:
                print("  ✅ Admin already exists")
            
            connection.commit()
            
            # ==========================================
            # 7. VERIFY
            # ==========================================
            print("\n" + "=" * 60)
            print("✅ Portfolio reseeded successfully!")
            
            cursor.execute("SELECT COUNT(*) FROM profiles")
            print(f"📊 Profiles: {cursor.fetchone()[0]}")
            
            cursor.execute("SELECT COUNT(*) FROM skills")
            print(f"📊 Skills: {cursor.fetchone()[0]}")
            
            cursor.execute("SELECT COUNT(*) FROM experiences")
            print(f"📊 Experiences: {cursor.fetchone()[0]}")
            
            cursor.execute("SELECT COUNT(*) FROM projects")
            print(f"📊 Projects: {cursor.fetchone()[0]}")
            
            cursor.execute("SELECT COUNT(*) FROM admins")
            print(f"📊 Admins: {cursor.fetchone()[0]}")
            
            print("\n📋 Experiences:")
            cursor.execute("SELECT company, position, is_current FROM experiences ORDER BY start_date DESC")
            for exp in cursor.fetchall():
                current = "⭐ CURRENT" if exp[2] else ""
                print(f"  {exp[1]} at {exp[0]} {current}")
            
            print("\n📋 Projects:")
            cursor.execute("SELECT title, featured FROM projects ORDER BY featured DESC")
            for proj in cursor.fetchall():
                featured = "⭐ FEATURED" if proj[1] else ""
                print(f"  {proj[0]} {featured}")
        
        connection.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    reseed_portfolio()