-- Database Schema for Portfolio Application
-- NIM: 2023XXXXX
-- Nama: Rezky Agung Kurniawan

CREATE DATABASE IF NOT EXISTS portfolio_db;
USE portfolio_db;

-- Profiles table
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
);

-- Skills table
CREATE TABLE IF NOT EXISTS skills (
    id INT PRIMARY KEY AUTO_INCREMENT,
    category VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL,
    icon VARCHAR(100),
    level INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Experiences table
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
);

-- Projects table
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
);

-- Contacts table
CREATE TABLE IF NOT EXISTS contacts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    subject VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Admins table
CREATE TABLE IF NOT EXISTS admins (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert initial profile
INSERT INTO profiles (name, title, about, email, phone, location, linkedin, github) 
VALUES (
    'Rezky Agung Kurniawan',
    'IT Infrastructure & Desktop Support Specialist',
    'Hi, I''m Rezky Agung Kurniawan, an IT Infrastructure & Desktop Support Specialist passionate about building reliable, secure, and efficient IT environments.

I have professional experience supporting enterprise infrastructure, managing Windows-based environments, deploying operating systems, administering Active Directory, monitoring network performance, and providing technical support for hundreds of end users. My background combines strong infrastructure knowledge with customer service experience, allowing me to communicate effectively while solving complex technical problems.

Currently, I work as an Infrastructure Support Specialist at Hejun Zongda Data Technology Co., Ltd., where I support enterprise infrastructure, manage Windows Server environments, deploy operating systems using Windows Deployment Services (WDS), administer Active Directory, monitor infrastructure with Zabbix, and manage incidents through ServiceNow.

Outside of my professional work, I actively build software projects to sharpen my development skills, combining infrastructure expertise with modern web technologies and AI.',
    'rezkytaewa2@gmail.com',
    '+62 822-5967-0594',
    'Sleman, Special Region of Yogyakarta, Indonesia',
    'https://www.linkedin.com/in/rezkytaewa',
    'https://github.com/Warfail'
);

-- Insert skills
INSERT INTO skills (category, name, level) VALUES
('Infrastructure & System Administration', 'Windows Server 2019', 85),
('Infrastructure & System Administration', 'Active Directory (AD)', 80),
('Infrastructure & System Administration', 'Group Policy (GPO)', 75),
('Infrastructure & System Administration', 'Windows Deployment Services (WDS)', 70),
('Infrastructure & System Administration', 'Windows Desktop Administration', 85),
('Infrastructure & System Administration', 'OS Deployment & Imaging', 75),
('Infrastructure & System Administration', 'IT Asset Lifecycle Management', 80),
('Infrastructure & System Administration', 'Enterprise Desktop Support', 85),
('Networking', 'TCP/IP Networking', 75),
('Networking', 'DNS & DHCP', 70),
('Networking', 'Basic Huawei Switch Configuration', 60),
('Networking', 'VLAN Fundamentals', 65),
('Networking', 'Network Troubleshooting', 80),
('Networking', 'Infrastructure Monitoring', 70),
('Networking', 'Zabbix Network Monitoring', 65),
('Virtualization', 'Oracle VM VirtualBox', 70),
('Virtualization', 'Virtual Machine Deployment', 75),
('Virtualization', 'Lab Environment Configuration', 70),
('IT Operations', 'ServiceNow (SNOW)', 75),
('IT Operations', 'Incident Management', 80),
('IT Operations', 'Change Management', 70),
('IT Operations', 'Asset Management', 75),
('IT Operations', 'End-user Support', 85),
('IT Operations', 'SLA Compliance', 80),
('IT Operations', 'Technical Documentation', 70),
('Development', 'JavaScript', 65),
('Development', 'React', 60),
('Development', 'Node.js', 60),
('Development', 'MongoDB', 55),
('Development', 'REST API Integration', 65),
('Development', 'Git & GitHub', 70),
('Soft Skills', 'Analytical Problem Solving', 85),
('Soft Skills', 'Communication', 80),
('Soft Skills', 'Team Collaboration', 80),
('Soft Skills', 'Customer Service', 85),
('Soft Skills', 'Time Management', 75),
('Soft Skills', 'Continuous Learning', 85);

-- Insert experiences
INSERT INTO experiences (company, position, location, start_date, end_date, is_current, description, achievements) VALUES
(
    'Hejun Zongda Data Technology Co., Ltd.',
    'Infrastructure Support Specialist',
    'Yogyakarta',
    '2025-09-01 00:00:00',
    NULL,
    TRUE,
    'Support infrastructure for approximately 350 enterprise workstations.',
    '["Managed infrastructure for 350+ workstations", "Implemented WDS for OS deployment", "Administered Active Directory and Group Policies", "Monitored infrastructure with Zabbix"]'
),
(
    'IGT Solutions',
    'Customer Service Representative',
    'Yogyakarta',
    '2025-02-01 00:00:00',
    '2025-09-01 00:00:00',
    FALSE,
    'Managed high-priority customer cases. Ensured compliance with operational procedures and SLA targets.',
    '["Awarded Best Supportive Agent", "Managed high-priority cases", "Maintained SLA compliance"]'
),
(
    'Teleperformance',
    'Infrastructure Desktop Support',
    'Jakarta',
    '2024-05-01 00:00:00',
    '2024-12-01 00:00:00',
    FALSE,
    'Provided internal desktop and infrastructure support. Diagnosed and resolved hardware, software, and networking issues.',
    '["Provided desktop and infrastructure support", "Resolved hardware, software, and networking issues", "Supported end users with workstation deployment"]'
),
(
    'Bursa Multimedia Group',
    'Desktop Support',
    'Yogyakarta',
    '2022-07-01 00:00:00',
    '2024-03-01 00:00:00',
    FALSE,
    'Managed approximately 1,500 IT assets. Supported multiple BPO clients as a third-party IT vendor.',
    '["Managed 1,500 IT assets", "Supported multiple BPO clients", "Performed hardware and network troubleshooting"]'
);

-- Insert projects
INSERT INTO projects (title, description, technologies, featured, project_url, github_url) VALUES
(
    'Restaurant POS System',
    'A full-stack Point of Sale (POS) system designed for restaurants, featuring order management, kitchen workflow, cashier operations, menu management, QR-code table ordering, and reporting dashboards.',
    '["React", "Node.js", "MongoDB", "REST API"]',
    TRUE,
    NULL,
    'https://github.com/Warfail'
),
(
    'AI Report Analyzer',
    'An AI-powered application that analyzes operational reports and automatically determines urgency levels for different departments, helping organizations prioritize incidents more efficiently.',
    '["Python", "AI/ML", "FastAPI", "React"]',
    TRUE,
    NULL,
    'https://github.com/Warfail'
),
(
    'Bursa Sewa Laptop',
    'A landing page for a laptop rental company. Built with modern web technologies and responsive design.',
    '["HTML", "CSS", "JavaScript", "Bootstrap"]',
    FALSE,
    'https://bursasewalaptop.github.io/',
    'https://github.com/Warfail'
);

-- Insert admin (password: admin123)
INSERT INTO admins (username, hashed_password) VALUES (
    'admin',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY3XhMKMhxTq5Ee'
);