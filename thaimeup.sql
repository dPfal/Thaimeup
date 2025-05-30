CREATE DATABASE  IF NOT EXISTS `thaimeup` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `thaimeup`;
-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: thaimeup
-- ------------------------------------------------------
-- Server version	8.0.42

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `category_id` int NOT NULL AUTO_INCREMENT,
  `category_name` varchar(50) NOT NULL,
  PRIMARY KEY (`category_id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES (2,'Noodle'),(3,'Entree'),(4,'Salad'),(5,'Curry'),(21,'Rice');
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `delivery_options`
--

DROP TABLE IF EXISTS `delivery_options`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `delivery_options` (
  `delivery_id` int NOT NULL AUTO_INCREMENT,
  `delivery_name` varchar(100) NOT NULL,
  `cost` decimal(10,2) DEFAULT '0.00',
  PRIMARY KEY (`delivery_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `delivery_options`
--

LOCK TABLES `delivery_options` WRITE;
/*!40000 ALTER TABLE `delivery_options` DISABLE KEYS */;
INSERT INTO `delivery_options` VALUES (1,'Standard',5.00),(2,'Express',10.00),(3,'Eco',3.00);
/*!40000 ALTER TABLE `delivery_options` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `items`
--

DROP TABLE IF EXISTS `items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `items` (
  `item_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `price` decimal(10,2) NOT NULL,
  `image` varchar(255) DEFAULT NULL,
  `category_id` int DEFAULT NULL,
  `is_available` tinyint(1) DEFAULT '1',
  `is_deleted` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`item_id`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `items_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`category_id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `items`
--

LOCK TABLES `items` WRITE;
/*!40000 ALTER TABLE `items` DISABLE KEYS */;
INSERT INTO `items` VALUES (1,'Pad Thai','Stir-fried rice noodles with tofu, shrimp, bean sprouts, peanuts, and tamarind sauce',20.90,'padthai.jpeg',2,0,0),(3,'Som Tum','Fresh shredded green papaya with chili, lime, fish sauce, tomatoes, and peanuts',17.90,'somtum.jpeg',4,1,0),(4,'Fried Rice','Fried jasmine rice with eggs, vegetables, and your choice of chicken, shrimp, or tofu',19.00,'friedrice.jpeg',21,1,0),(5,'Roti','Hot Roti',3.00,'roti.jpeg',3,1,0),(6,'Springrolls','Vegetable Springrolls (4pcs)',12.50,'springrolls.jpeg',3,1,0),(7,'Green Curry','Spicy green curry with chicken, eggplant, bamboo shoots, and basil in coconut milk',23.00,'greencurry.jpeg',5,1,0),(8,'Massaman Curry','Rich, mild curry made with beef, potatoes, peanuts, and a touch of cinnamon',24.00,'massaman.jpeg',5,1,0),(9,'Panang Curry','Thick, creamy red curry with beef or chicken, bell peppers, and kaffir lime leaves',21.50,'panang.jpeg',5,1,0),(10,'Thai Fish Cakes','Spicy fish patties with red curry paste and kaffir lime leaves, served with sweet chili sauce',13.90,'fishcake.jpeg',3,1,0),(11,'Tom Yum Soup','Hot and sour soup with shrimp, lemongrass, galangal, lime leaves, and chili',19.50,'tomyum.jpeg',3,1,0),(12,'Larb','Spicy minced chicken salad with lime juice, chili, mint, and roasted rice powder',18.00,'larb.jpeg',4,1,0),(13,'Mango Sticky Rice','Sweet sticky rice served with fresh mango and coconut cream',14.00,'mangosticky.jpeg',3,1,0),(14,'Pad Kee Mao','Spicy stir-fried rice noodles with chili, garlic, basil, and vegetables',21.00,'padkeemao.jpeg',2,1,0),(15,'Thai Satay','Grilled marinated chicken skewers served with peanut sauce and cucumber relish',16.50,'satay.jpeg',3,1,0),(25,'Khao khluk kapi','Fried rice made with shrimp paste and topped with crispy dried shrimps, dried mango gratings, omelet shavings, chilies, cucumbers, red and green onions.',21.00,'khaokhlukkapi.jpeg',21,1,1),(26,'Khanom jeeb','Dumplings stuffed with pork and shrimp paste.\r\n',7.00,'khanomjeeb.jpeg',3,1,1),(27,'Flan','dessert',9.00,'flan.jpeg',2,1,1);
/*!40000 ALTER TABLE `items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_items`
--

DROP TABLE IF EXISTS `order_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_items` (
  `order_item_id` int NOT NULL AUTO_INCREMENT,
  `order_id` int DEFAULT NULL,
  `item_id` int DEFAULT NULL,
  `quantity` int NOT NULL,
  PRIMARY KEY (`order_item_id`),
  KEY `order_id` (`order_id`),
  KEY `item_id` (`item_id`),
  CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`),
  CONSTRAINT `order_items_ibfk_2` FOREIGN KEY (`item_id`) REFERENCES `items` (`item_id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_items`
--

LOCK TABLES `order_items` WRITE;
/*!40000 ALTER TABLE `order_items` DISABLE KEYS */;
INSERT INTO `order_items` VALUES (1,1,4,2),(2,1,8,1),(3,2,11,1),(4,2,6,2),(5,2,7,1),(6,3,9,2),(13,10,25,2),(14,11,26,4);
/*!40000 ALTER TABLE `order_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `order_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `order_date_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `delivery_id` int DEFAULT NULL,
  `recipient_phone` varchar(20) NOT NULL,
  `recipient_address` text NOT NULL,
  `recipient_first_name` varchar(100) NOT NULL,
  `recipient_last_name` varchar(100) NOT NULL,
  `status` varchar(50) DEFAULT 'PENDING',
  `payment_method` varchar(50) NOT NULL,
  PRIMARY KEY (`order_id`),
  KEY `user_id` (`user_id`),
  KEY `delivery_id` (`delivery_id`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`delivery_id`) REFERENCES `delivery_options` (`delivery_id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (1,2,'2025-05-27 16:14:02',1,'123456789','shop 1356/2049 Logan Road','regular','regular','COMPLETED','PayPal'),(2,3,'2025-05-27 16:14:41',2,'1235123623','694 Brunswick Street, New Farm','regular2','regular2','CANCELLED','Apple Pay'),(3,4,'2025-05-27 16:15:29',3,'1235124623','P block 2 George Street, Brisbane City QLD 4000, Australia','regular3','regular3','PENDING','Credit/Debit Card'),(10,2,'2025-05-30 15:56:01',1,'123456789','7 Waterford Street, Alderley, QLD, 4051','regular','regular','COMPLETED','PayPal'),(11,2,'2025-05-30 15:56:15',1,'123456789','7 Waterford Street, Alderley, QLD, 4051','regular','regular','CANCELLED','PayPal');
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `email` varchar(100) NOT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `is_admin` tinyint(1) DEFAULT '0',
  `phone` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (2,'regular1','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','regular1@gmail.com','regular','regular',0,'123456789'),(3,'regular2','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','regular2@gmail.com','regular2','regular2',0,'1235123623'),(4,'regular3','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','regular3@gmail.com','regular3','regular3',0,'1235124623'),(5,'admin1','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','admin@gmail.com','admin','admin',1,'1235123656'),(6,'admin2','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','admin2@gmail.com','admin2','admin2',1,'1231246234');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-30 17:00:57
