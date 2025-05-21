
DROP TABLE IF EXISTS `categories`;
CREATE TABLE `categories` (
  `category_id` int NOT NULL AUTO_INCREMENT,
  `category_name` varchar(50) NOT NULL,
  PRIMARY KEY (`category_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `categories` WRITE;
INSERT INTO `categories` VALUES (1,'Rice'),(2,'Noodle'),(3,'Entree'),(4,'Salad'),(5,'Curry');
UNLOCK TABLES;
DROP TABLE IF EXISTS `delivery_options`;
CREATE TABLE `delivery_options` (
  `delivery_id` int NOT NULL AUTO_INCREMENT,
  `delivery_name` varchar(100) NOT NULL,
  `cost` decimal(10,2) DEFAULT '0.00',
  PRIMARY KEY (`delivery_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `delivery_options` WRITE;
INSERT INTO `delivery_options` VALUES (1,'Standard',5.00),(2,'Express',10.00),(3,'Eco',3.00);
UNLOCK TABLES;
DROP TABLE IF EXISTS `items`;
CREATE TABLE `items` (
  `item_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `price` decimal(10,2) NOT NULL,
  `image` varchar(255) DEFAULT NULL,
  `category_id` int DEFAULT NULL,
  `is_available` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`item_id`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `items_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`category_id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `items` WRITE;
INSERT INTO `items` VALUES (1,'Pad Thai','Stir-fried rice noodles with tofu, shrimp, bean sprouts, peanuts, and tamarind sauce',20.90,'padthai.jpeg',2,0),(2,'Pad Se Ew','Fat rice noodle stir fried in soy and oyster sauce with Asian greens',21.90,'padseew.jpeg',2,0),(3,'Som Tum','Fresh shredded green papaya with chili, lime, fish sauce, tomatoes, and peanuts',17.90,'somtum.jpeg',4,1),(4,'Fried Rice','Fried jasmine rice with eggs, vegetables, and your choice of chicken, shrimp, or tofu',19.00,'friedrice.jpeg',1,1),(5,'Roti','Hot Roti',3.00,'roti.jpeg',3,1),(6,'Springrolls','Vegetable Springrolls (4pcs)',12.50,'springrolls.jpeg',3,1),(7,'Green Curry','Spicy green curry with chicken, eggplant, bamboo shoots, and basil in coconut milk',23.00,'greencurry.jpeg',5,1),(8,'Massaman Curry','Rich, mild curry made with beef, potatoes, peanuts, and a touch of cinnamon',24.00,'massaman.jpeg',5,1),(9,'Panang Curry','Thick, creamy red curry with beef or chicken, bell peppers, and kaffir lime leaves',21.50,'panang.jpeg',5,1),(10,'Thai Fish Cakes','Spicy fish patties with red curry paste and kaffir lime leaves, served with sweet chili sauce',13.90,'fishcake.jpeg',3,1),(11,'Tom Yum Soup','Hot and sour soup with shrimp, lemongrass, galangal, lime leaves, and chili',19.50,'tomyum.jpeg',3,1),(12,'Larb','Spicy minced chicken salad with lime juice, chili, mint, and roasted rice powder',18.00,'larb.jpeg',4,1),(13,'Mango Sticky Rice','Sweet sticky rice served with fresh mango and coconut cream',14.00,'mangosticky.jpeg',3,1),(14,'Pad Kee Mao','Spicy stir-fried rice noodles with chili, garlic, basil, and vegetables',21.00,'padkeemao.jpeg',2,1),(15,'Thai Satay','Grilled marinated chicken skewers served with peanut sauce and cucumber relish',16.50,'satay.jpeg',3,1);
UNLOCK TABLES;
DROP TABLE IF EXISTS `order_items`;
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
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `order_items` WRITE;
UNLOCK TABLES;
DROP TABLE IF EXISTS `orders`;
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
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `orders` WRITE;
UNLOCK TABLES;
DROP TABLE IF EXISTS `users`;
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
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `users` WRITE;
UNLOCK TABLES;