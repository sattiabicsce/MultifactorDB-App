-- Create the database
DROP DATABASE IF EXISTS SmartDeviceManagement;
CREATE DATABASE SmartDeviceManagement;
USE SmartDeviceManagement;

CREATE TABLE Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(255),
    LastName VARCHAR(255),
    Username VARCHAR(255),
    Password VARCHAR(255), 
    JobTitle VARCHAR(255),
    ClearanceLevel ENUM('TS', 'S', 'P', 'NA'),
    Role ENUM('Admin', 'Owner', 'DataWriter') NOT NULL
);

CREATE TABLE SmartPhones (
    DeviceID INT AUTO_INCREMENT PRIMARY KEY,
    PhoneNumber VARCHAR(20) CHECK (PhoneNumber LIKE '(_)%'),
    SimCard TINYINT,
    UserID INT,
    OwnerID INT,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

CREATE TABLE AuthenticationFactor (
    AuthFactorID INT AUTO_INCREMENT PRIMARY KEY,
    AuthFactorName VARCHAR(255),
    Security TINYINT CHECK (Security BETWEEN 1 AND 10),
    Intrusiveness TINYINT CHECK (Intrusiveness BETWEEN 1 AND 10),
    Accuracy TINYINT CHECK (Accuracy BETWEEN 1 AND 10),
    Privacy TINYINT CHECK (Privacy BETWEEN 1 AND 10),
    Passive TINYINT CHECK (Passive IN (0, 1)),
    Effort TINYINT CHECK (Effort BETWEEN 0 AND 10),
    UserPref VARCHAR(255),
    DeviceID INT,
    FOREIGN KEY (DeviceID) REFERENCES SmartPhones(DeviceID)
);

CREATE TABLE SmartPhoneDetails (
    DetailID INT AUTO_INCREMENT PRIMARY KEY,
    DeviceID INT,
    Latitude DECIMAL(10, 6),
    Longitude DECIMAL(10, 6),
    ipString VARCHAR(15), -- Changed from CurrentIP to ipString
    CurrentTime DATETIME,
    AvailableMemory BIGINT,
    RSSI INT,
    Timezone VARCHAR(50),
    Processors INT,
    Battery INT,
    Vendor VARCHAR(50),
    Model VARCHAR(50),
    SystemPerformance INT,
    CPU VARCHAR(50),
    Accel INT,
    Gyro INT,
    Magnet INT,
    CurrentWifi VARCHAR(255),
    ScreenWidth INT,
    ScreenLength INT,
    ScreenDensity INT,
    AuthenticationFeatures VARCHAR(255),
    hasTouchScreen BOOLEAN, -- Added boolean for Touch Screen
    hasCamera BOOLEAN,      -- Added boolean for Camera
    hasFrontCamera BOOLEAN, -- Added boolean for Front Camera
    hasMicrophone BOOLEAN,  -- Added boolean for Microphone
    hasTemperatureSensor BOOLEAN, -- Added boolean for Temperature Sensor
    FOREIGN KEY (DeviceID) REFERENCES SmartPhones(DeviceID)
);

-- Insert Users with Roles
INSERT INTO Users (FirstName, LastName, Username, Password, JobTitle, ClearanceLevel, Role) VALUES
('Alice', 'Popp', 'apopp', 'password123', 'Engineer', 'TS', 'Admin'),
('Bob', 'Smith', 'bsmith', 'password456', 'Manager', 'S', 'Owner'),
('Charlie', 'Jones', 'cjones', 'password789', 'Technician', 'P', 'Owner'),
('David', 'Johnson', 'djohnson', 'password101', 'Analyst', 'NA', 'DataWriter'),
('Eve', 'Brown', 'ebrown', 'password202', 'Designer', 'TS', 'Admin'),
('Frank', 'White', 'fwhite', 'password303', 'Developer', 'S', 'DataWriter');

INSERT INTO SmartPhones (DeviceID, PhoneNumber, SimCard, UserID, OwnerID) VALUES
(1, '(1)8037775679', 1, 2, 2),
(2, '(1)8037775680', 0, 2, 2),
(3, '(1)8037775681', 1, 3, 3),
(4, '(1)8037775682', 0, 3, 3),
(5, '(1)8037775683', 1, 3, 3),
(6, '(1)8037775684', 1, 4, 4),
(7, '(1)8037775685', 0, 5, 5),
(8, '(1)8037775686', 1, 6, 6),
(9, '(1)8037775687', 0, 6, 6),
(10, '(1)8037775688', 1, 6, 6);

-- Example insert into SmartPhoneDetails
INSERT INTO SmartPhoneDetails (
    DeviceID, Latitude, Longitude, ipString, CurrentTime, AvailableMemory, RSSI, Timezone, Processors, Battery, Vendor, Model, 
    SystemPerformance, CPU, Accel, Gyro, Magnet, CurrentWifi, ScreenWidth, ScreenLength, ScreenDensity, AuthenticationFeatures, 
    hasTouchScreen, hasCamera, hasFrontCamera, hasMicrophone, hasTemperatureSensor
) VALUES
    (1, 55.13974, -122.380566, '10.0.2.246', '2024-05-15 08:59:00', 1018953353, -43, 'America/New_York', 4, 26, 'Google', 'sdk_gphone64_x86_64', 
     4, 'ranchu', 1, 4, 2, '[AndroidWifi]', 1080, 2337, 420, 'RandomAuthenticationFeatures', TRUE, TRUE, TRUE, TRUE, FALSE),
     
    (2, 35.6895, 139.6917, '192.168.1.2', '2024-06-15 10:00:00', 2048000, -50, 'Asia/Tokyo', 8, 50, 'Apple', 'iPhone 13', 
     9, 'A15 Bionic', 1, 1, 1, 'TokyoWifi', 1170, 2532, 460, 'FaceID', TRUE, TRUE, TRUE, TRUE, FALSE),
     
    (3, 37.7749, -122.4194, '192.168.1.3', '2024-06-15 11:00:00', 4096000, -55, 'America/Los_Angeles', 8, 70, 'Samsung', 'Galaxy S21', 
     8, 'Exynos 2100', 1, 1, 1, 'SFWifi', 1080, 2400, 450, 'Fingerprint', TRUE, TRUE, TRUE, TRUE, FALSE),
     
    (4, 48.8566, 2.3522, '192.168.1.4', '2024-06-15 12:00:00', 3072000, -60, 'Europe/Paris', 6, 30, 'Google', 'Pixel 6', 
     7, 'Tensor', 1, 1, 1, 'ParisWifi', 1080, 2400, 420, 'Pattern', TRUE, TRUE, TRUE, TRUE, FALSE),
     
    (5, 40.7128, -74.0060, '192.168.1.5', '2024-06-15 13:00:00', 1024000, -65, 'America/New_York', 4, 20, 'OnePlus', 'OnePlus 9', 
     7, 'Snapdragon 888', 1, 1, 1, 'NYWifi', 1080, 2400, 410, 'Password', TRUE, TRUE, TRUE, TRUE, TRUE),
     
    (6, 34.0522, -118.2437, '192.168.1.6', '2024-06-15 14:00:00', 512000, -70, 'America/Los_Angeles', 4, 10, 'Huawei', 'P50 Pro', 
     6, 'Kirin 9000', 1, 1, 1, 'LAWIFI', 1080, 2400, 400, 'Iris Scan', TRUE, TRUE, TRUE, TRUE, FALSE),
     
    (7, 51.5074, -0.1278, '192.168.1.7', '2024-06-15 15:00:00', 2048000, -75, 'Europe/London', 8, 50, 'Apple', 'iPhone 12', 
     8, 'A14 Bionic', 1, 1, 1, 'LondonWifi', 1170, 2532, 460, 'FaceID', TRUE, TRUE, TRUE, TRUE, TRUE),
     
    (8, 55.7558, 37.6176, '192.168.1.8', '2024-06-15 16:00:00', 1024000, -80, 'Europe/Moscow', 4, 40, 'Google', 'Pixel 5', 
     7, 'Snapdragon 765G', 1, 1, 1, 'MoscowWifi', 1080, 2340, 410, 'Fingerprint', TRUE, TRUE, TRUE, TRUE, FALSE),
     
    (9, 28.6139, 77.2090, '192.168.1.9', '2024-06-15 17:00:00', 2048000, -85, 'Asia/Kolkata', 6, 30, 'Samsung', 'Galaxy S20', 
     8, 'Exynos 990', 1, 1, 1, 'DelhiWifi', 1080, 2400, 450, 'Pattern', TRUE, TRUE, TRUE, TRUE, TRUE),
     
    (10, -33.8688, 151.2093, '192.168.1.10', '2024-06-15 18:00:00', 4096000, -90, 'Australia/Sydney', 8, 70, 'OnePlus', 'OnePlus 8', 
     9, 'Snapdragon 865', 1, 1, 1, 'SydneyWifi', 1080, 2400, 420, 'Password', TRUE, TRUE, TRUE, TRUE, TRUE);

-- Insert into AuthenticationFactor
INSERT INTO AuthenticationFactor (AuthFactorName, Security, Intrusiveness, Accuracy, Privacy, Passive, Effort, UserPref, DeviceID) VALUES 
('RandomAuthenticationFeatures', 8, 3, 7, 9, 0, 5, 'User Preference 1', 1),
('FaceID', 9, 3, 9, 7, 0, 5, 'User Preference 2', 2),
('Fingerprint', 8, 3, 8, 6, 1, 3, 'User Preference 3', 3),
('Pattern', 6, 2, 7, 5, 1, 4, 'User Preference 4', 4),
('Password', 5, 1, 7, 6, 0, 2, 'User Preference 5', 5),
('Iris Scan', 8, 4, 9, 7, 0, 6, 'User Preference 6', 6),
('FaceID', 5, 7, 7, 9, 0, 7, 'User Preference 7', 7),
('Fingerprint', 5, 4, 3, 7, 1, 4, 'User Preference 8', 8),
('Pattern', 6, 8, 9, 7, 1, 5, 'User Preference 9', 9),
('Password', 4, 2, 5, 4, 0, 3, 'User Preference 10', 10);

-- Creating MySQL users for each role
DROP USER IF EXISTS 'admin_user'@'localhost';
DROP USER IF EXISTS 'owner_user'@'localhost';
DROP USER IF EXISTS 'data_writer_user'@'localhost';

CREATE USER 'admin_user'@'localhost' IDENTIFIED BY 'admin_password';
CREATE USER 'owner_user'@'localhost' IDENTIFIED BY 'owner_password';
CREATE USER 'data_writer_user'@'localhost' IDENTIFIED BY 'data_writer_password';

-- Grant privileges
-- Admin User
GRANT ALL PRIVILEGES ON SmartDeviceManagement.* TO 'admin_user'@'localhost';

-- Data Writer User
GRANT SELECT, INSERT, UPDATE ON SmartDeviceManagement.* TO 'data_writer_user'@'localhost';

-- Create a view for Owners to see their own data
CREATE VIEW OwnerSmartPhones AS
SELECT * FROM SmartPhones WHERE OwnerID = (SELECT UserID FROM Users WHERE Username = SUBSTRING_INDEX(USER(),'@',1));

-- Grant SELECT privilege on this view to owner_user
GRANT SELECT ON SmartDeviceManagement.OwnerSmartPhones TO 'owner_user'@'localhost';

DELIMITER //
CREATE PROCEDURE InsertSmartPhone(
    IN phoneNumber VARCHAR(20),
    IN simCard TINYINT,
    IN userID INT
)
BEGIN
    INSERT INTO SmartPhones (PhoneNumber, SimCard, UserID, OwnerID)
    VALUES (phoneNumber, simCard, userID, (SELECT UserID FROM Users WHERE Username = SUBSTRING_INDEX(USER(),'@',1)));
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE UpdateSmartPhone(
    IN deviceID INT,
    IN phoneNumber VARCHAR(20),
    IN simCard TINYINT
)
BEGIN
    UPDATE SmartPhones
    SET PhoneNumber = phoneNumber, SimCard = simCard
    WHERE DeviceID = deviceID AND OwnerID = (SELECT UserID FROM Users WHERE Username = SUBSTRING_INDEX(USER(),'@',1));
END //
DELIMITER ;

DELIMITER //

CREATE PROCEDURE GetRandomValidAuthFactors(
    IN inputUsername VARCHAR(255)
)
BEGIN
    -- Declare variables
    DECLARE random_limit INT DEFAULT 0;
    DECLARE sql_query TEXT;

    -- Create the temporary table for all authentication factors
    CREATE TEMPORARY TABLE TempUserAuthFactors (
        FirstName VARCHAR(255),
        LastName VARCHAR(255),
        DeviceID INT,
        PhoneNumber VARCHAR(20),
        AuthenticationFactorName VARCHAR(255),
        Security TINYINT,
        Intrusiveness TINYINT,
        Accuracy TINYINT,
        Privacy TINYINT
    );

    -- Insert data into the temporary table
    INSERT INTO TempUserAuthFactors (FirstName, LastName, DeviceID, PhoneNumber, AuthenticationFactorName, Security, Intrusiveness, Accuracy, Privacy)
    SELECT
        u.FirstName,
        u.LastName,
        sp.DeviceID,
        sp.PhoneNumber,
        af.AuthFactorName,
        af.Security,
        af.Intrusiveness,
        af.Accuracy,
        af.Privacy
    FROM
        Users u
    JOIN
        SmartPhones sp ON u.UserID = sp.OwnerID
    JOIN
        SmartPhoneDetails spd ON sp.DeviceID = spd.DeviceID
    JOIN
        AuthenticationFactor af ON spd.DeviceID = af.DeviceID
    WHERE
        u.Username = inputUsername;

    -- Create the table for valid authentication factors
    CREATE TEMPORARY TABLE ValidAuthFactors (
        FirstName VARCHAR(255),
        LastName VARCHAR(255),
        DeviceID INT,
        PhoneNumber VARCHAR(20),
        AuthenticationFactorName VARCHAR(255),
        Security TINYINT,
        Intrusiveness TINYINT,
        Accuracy TINYINT,
        Privacy TINYINT
    );

    -- Insert data into the ValidAuthFactors table where all values are 5 or above
    INSERT INTO ValidAuthFactors (FirstName, LastName, DeviceID, PhoneNumber, AuthenticationFactorName, Security, Intrusiveness, Accuracy, Privacy)
    SELECT
        FirstName,
        LastName,
        DeviceID,
        PhoneNumber,
        AuthenticationFactorName,
        Security,
        Intrusiveness,
        Accuracy,
        Privacy
    FROM
        TempUserAuthFactors
    WHERE
        Security >= 5 AND
        Intrusiveness >= 5 AND
        Accuracy >= 5 AND
        Privacy >= 5;

    -- Set the random limit to a random number between 1 and the count of ValidAuthFactors
    SET random_limit = FLOOR(1 + RAND() * (SELECT COUNT(*) FROM ValidAuthFactors));

    -- Create the table for random selection of valid authentication factors using dynamic SQL
    SET sql_query = CONCAT('CREATE TEMPORARY TABLE RandomValidAuthFactors AS SELECT * FROM ValidAuthFactors ORDER BY RAND() LIMIT ', random_limit);
    PREPARE stmt FROM @sql_query;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;

    -- Select data from the RandomValidAuthFactors table
    SELECT * FROM RandomValidAuthFactors;
END //

DELIMITER ;
