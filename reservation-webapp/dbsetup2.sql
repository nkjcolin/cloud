/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

DROP DATABASE IF EXISTS `clouddb2`;
CREATE DATABASE IF NOT EXISTS `clouddb2` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `clouddb2`;

DROP TABLE IF EXISTS particulars;
CREATE TABLE IF NOT EXISTS particulars (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50) NOT NULL DEFAULT '0',
  phone VARCHAR(50) NOT NULL DEFAULT '0',
  email VARCHAR(50) NOT NULL DEFAULT '0',
  size INT NOT NULL DEFAULT 0
) ENGINE=InnoDB;

DROP TABLE IF EXISTS restaurants;
CREATE TABLE IF NOT EXISTS restaurants (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50) NOT NULL DEFAULT '0',
  dietary_needs VARCHAR(50) NOT NULL DEFAULT '0',
  meal_type VARCHAR(50) NOT NULL DEFAULT '0',
  timings JSON, -- Use JSON data type for storing an array of timings
  description TEXT -- Add a description column
) ENGINE=InnoDB;

INSERT INTO restaurants (name, dietary_needs, meal_type, timings, description)
VALUES
    ('Restaurant 1', 'Healthy', 'Light', '["12:00 PM", "1:00 PM", "7:00 PM"]', 'Description 1'),
    ('Restaurant 2', 'Healthy', 'Medium', '["11:30 AM", "2:30 PM", "8:00 PM"]', 'Description 2');
    ('Restaurant 3', 'Healthy', 'Light', '["11:30 AM", "2:30 PM", "8:00 PM"]', 'Description 3');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
