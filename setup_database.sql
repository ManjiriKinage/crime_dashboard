-- ==============================================
-- Crime Record Management System - Database Setup
-- ==============================================

-- Create Database
CREATE DATABASE IF NOT EXISTS crime_db;
USE crime_db;

-- ==============================================
-- Police Officers Table (Authentication)
-- ==============================================

CREATE TABLE IF NOT EXISTS police_officers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    badge_number VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_badge (badge_number)
);

-- ==============================================
-- Crime Records Table
-- ==============================================

CREATE TABLE IF NOT EXISTS crimes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL,
    gender VARCHAR(20),
    weapon VARCHAR(100),
    recorded_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (recorded_by) REFERENCES police_officers(id),
    INDEX idx_city (city),
    INDEX idx_type (type),
    INDEX idx_date (date),
    INDEX idx_gender (gender)
);

-- ==============================================
-- Sample Data - Police Officers (TEST ONLY)
-- ==============================================

INSERT INTO police_officers (username, password, name, badge_number, email) VALUES
('officer_01', 'pass123', 'Raj Kumar', 'PB001', 'raj.kumar@police.gov.in'),
('officer_02', 'pass123', 'Priya Singh', 'PB002', 'priya.singh@police.gov.in'),
('officer_03', 'pass123', 'Amit Patel', 'PB003', 'amit.patel@police.gov.in');

-- ==============================================
-- Sample Data - Crime Records
-- ==============================================

INSERT INTO crimes (type, city, date, time, gender, weapon, recorded_by) VALUES
('Theft', 'Mumbai', '2024-01-15', '14:30:00', 'Male', 'Knife', 1),
('Robbery', 'Delhi', '2024-01-14', '22:45:00', 'Female', 'Gun', 2),
('Assault', 'Bangalore', '2024-01-13', '10:15:00', 'Male', 'Baseball Bat', 3),
('Murder', 'Chennai', '2024-01-12', '23:30:00', 'Female', 'Knife', 1),
('Fraud', 'Hyderabad', '2024-01-11', '09:00:00', 'Other', 'Poison', 2),
('Burglary', 'Pune', '2024-01-10', '03:00:00', 'Male', 'Stone', 3),
('Drug Trafficking', 'Kolkata', '2024-01-09', '18:20:00', 'Male', 'Gun', 1),
('Assault', 'Mumbai', '2024-01-08', '16:45:00', 'Female', 'Hammer', 2),
('Theft', 'Delhi', '2024-01-07', '12:00:00', 'Female', 'Knife', 3),
('Robbery', 'Bangalore', '2024-01-06', '20:30:00', 'Male', 'Sword', 1);

-- ==============================================
-- Queries for Verification
-- ==============================================

-- Check Police Officers
SELECT * FROM police_officers;

-- Check Crime Records
SELECT * FROM crimes;

-- Crime Count by City
SELECT city, COUNT(*) as crime_count FROM crimes GROUP BY city;

-- Crime Count by Type
SELECT type, COUNT(*) as crime_count FROM crimes GROUP BY type;

-- Gender Distribution
SELECT gender, COUNT(*) as count FROM crimes GROUP BY gender;

-- Weapon Usage
SELECT weapon, COUNT(*) as count FROM crimes GROUP BY weapon;
