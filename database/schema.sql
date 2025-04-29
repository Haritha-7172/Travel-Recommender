-- Travel Recommender Database Schema

-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS travel_recommender;
USE travel_recommender;

-- User Table
CREATE TABLE IF NOT EXISTS User (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    dest_pref VARCHAR(100),
    Bud_pref VARCHAR(100)
);

-- Destination Table
CREATE TABLE IF NOT EXISTS Destination (
    dest_id INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Type VARCHAR(50) NOT NULL,
    avg_cost DECIMAL(10, 2) NOT NULL
);

-- Accommodation Table
CREATE TABLE IF NOT EXISTS Accommodation (
    Acc_id INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    cost_per_night DECIMAL(10, 2) NOT NULL
);

-- Budget Table
CREATE TABLE IF NOT EXISTS Budget (
    Bud_id INT AUTO_INCREMENT PRIMARY KEY,
    duration INT NOT NULL,
    total_bud DECIMAL(10, 2) NOT NULL
);

-- Activities Table
CREATE TABLE IF NOT EXISTS Activities (
    Act_name VARCHAR(100),
    Act_cost DECIMAL(10, 2) NOT NULL,
    dest_id INT,
    PRIMARY KEY (Act_name, dest_id),
    FOREIGN KEY (dest_id) REFERENCES Destination(dest_id) ON DELETE CASCADE
);

-- Likes Relationship (User likes Destination)
CREATE TABLE IF NOT EXISTS Likes (
    user_id INT,
    dest_id INT,
    PRIMARY KEY (user_id, dest_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
    FOREIGN KEY (dest_id) REFERENCES Destination(dest_id) ON DELETE CASCADE
);

-- Chooses Relationship (User chooses Budget with climate preference)
CREATE TABLE IF NOT EXISTS Chooses (
    user_id INT,
    Bud_id INT,
    dest_id INT,
    climate VARCHAR(50) NOT NULL,
    PRIMARY KEY (user_id, Bud_id, dest_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
    FOREIGN KEY (Bud_id) REFERENCES Budget(Bud_id) ON DELETE CASCADE,
    FOREIGN KEY (dest_id) REFERENCES Destination(dest_id) ON DELETE CASCADE
);

-- Stays Relationship (Destination has Accommodation)
CREATE TABLE IF NOT EXISTS stays (
    dest_id INT,
    Acc_id INT,
    location_of_place VARCHAR(100) NOT NULL,
    PRIMARY KEY (dest_id, Acc_id),
    FOREIGN KEY (dest_id) REFERENCES Destination(dest_id) ON DELETE CASCADE,
    FOREIGN KEY (Acc_id) REFERENCES Accommodation(Acc_id) ON DELETE CASCADE
);

-- Owns Relationship (User owns Accommodation with room size)
CREATE TABLE IF NOT EXISTS owns (
    user_id INT,
    Acc_id INT,
    Bud_id INT,
    room_size VARCHAR(50) NOT NULL,
    PRIMARY KEY (user_id, Acc_id, Bud_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
    FOREIGN KEY (Acc_id) REFERENCES Accommodation(Acc_id) ON DELETE CASCADE,
    FOREIGN KEY (Bud_id) REFERENCES Budget(Bud_id) ON DELETE CASCADE
);

-- Indexes for better query performance
CREATE INDEX idx_dest_type ON Destination(Type);
CREATE INDEX idx_acc_type ON Accommodation(type);
CREATE INDEX idx_budget_duration ON Budget(duration);
CREATE INDEX idx_budget_total ON Budget(total_bud);
CREATE INDEX idx_chooses_climate ON Chooses(climate);
