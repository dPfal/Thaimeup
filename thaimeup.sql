CREATE DATABASE IF NOT EXISTS thaimeup;
USE thaimeup;

DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS delivery_options;
DROP TABLE IF EXISTS users;

CREATE TABLE categories (
  category_id INT NOT NULL AUTO_INCREMENT,
  category_name VARCHAR(50) NOT NULL,
  is_deleted TINYINT(1) DEFAULT 0,
  PRIMARY KEY (category_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO categories VALUES
(1, 'Noodle', 0),
(2, 'Entree', 0),
(3, 'Salad', 0),
(4, 'Curry', 0),
(5, 'Rice', 0);

CREATE TABLE delivery_options (
  delivery_id INT NOT NULL AUTO_INCREMENT,
  delivery_name VARCHAR(100) NOT NULL,
  cost DECIMAL(10,2) DEFAULT 0.00,
  PRIMARY KEY (delivery_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO delivery_options VALUES
(1, 'Standard', 5.00),
(2, 'Express', 10.00),
(3, 'Eco', 3.00);

CREATE TABLE users (
  user_id INT NOT NULL AUTO_INCREMENT,
  username VARCHAR(50) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  email VARCHAR(100) NOT NULL,
  first_name VARCHAR(50),
  last_name VARCHAR(50),
  is_admin TINYINT(1) DEFAULT 0,
  phone VARCHAR(20),
  PRIMARY KEY (user_id),
  UNIQUE (username),
  UNIQUE (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO users VALUES
(2,'regular1','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','regular1@gmail.com','regular','regular',0,'123456789'),
(3,'regular2','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','regular2@gmail.com','regular2','regular2',0,'1235123623'),
(4,'regular3','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','regular3@gmail.com','regular3','regular3',0,'1235124623'),
(5,'admin1','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','admin@gmail.com','admin','admin',1,'1235123656'),
(6,'admin2','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','admin2@gmail.com','admin2','admin2',1,'1231246234');

CREATE TABLE items (
  item_id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  description VARCHAR(255),
  price DECIMAL(10,2) NOT NULL,
  image VARCHAR(255),
  category_id INT,
  is_available TINYINT(1) DEFAULT 1,
  is_deleted TINYINT(1) DEFAULT 0,
  PRIMARY KEY (item_id),
  FOREIGN KEY (category_id) REFERENCES categories(category_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO items (name, description, price, image, category_id, is_available, is_deleted) VALUES
('Pad Thai','Stir-fried rice noodles with tofu, shrimp, bean sprouts, peanuts, and tamarind sauce',20.90,'padthai.jpeg',1,0,0),
('Som Tum','Fresh shredded green papaya with chili, lime, fish sauce, tomatoes, and peanuts',17.90,'somtum.jpeg',3,1,0),
('Fried Rice','Fried jasmine rice with eggs, vegetables, and your choice of chicken, shrimp, or tofu',19.00,'friedrice.jpeg',5,1,0),
('Roti','Hot Roti',3.00,'roti.jpeg',2,1,0),
('Springrolls','Vegetable Springrolls (4pcs)',12.50,'springrolls.jpeg',2,1,0),
('Green Curry','Spicy green curry with chicken, eggplant, bamboo shoots, and basil in coconut milk',23.00,'greencurry.jpeg',4,1,0),
('Massaman Curry','Rich, mild curry made with beef, potatoes, peanuts, and a touch of cinnamon',24.00,'massaman.jpeg',4,1,0),
('Panang Curry','Thick, creamy red curry with beef or chicken, bell peppers, and kaffir lime leaves',21.50,'panang.jpeg',4,1,0),
('Thai Fish Cakes','Spicy fish patties with red curry paste and kaffir lime leaves, served with sweet chili sauce',13.90,'fishcake.jpeg',2,1,0),
('Tom Yum Soup','Hot and sour soup with shrimp, lemongrass, galangal, lime leaves, and chili',19.50,'tomyum.jpeg',2,1,0),
('Larb','Spicy minced chicken salad with lime juice, chili, mint, and roasted rice powder',18.00,'larb.jpeg',3,1,0),
('Mango Sticky Rice','Sweet sticky rice served with fresh mango and coconut cream',14.00,'mangosticky.jpeg',2,1,0),
('Pad Kee Mao','Spicy stir-fried rice noodles with chili, garlic, basil, and vegetables',21.00,'padkeemao.jpeg',1,1,0),
('Thai Satay','Grilled marinated chicken skewers served with peanut sauce and cucumber relish',16.50,'satay.jpeg',2,1,0);

CREATE TABLE orders (
  order_id INT NOT NULL AUTO_INCREMENT,
  user_id INT,
  order_date_time DATETIME DEFAULT CURRENT_TIMESTAMP,
  delivery_id INT,
  recipient_phone VARCHAR(20) NOT NULL,
  recipient_address TEXT NOT NULL,
  recipient_first_name VARCHAR(100) NOT NULL,
  recipient_last_name VARCHAR(100) NOT NULL,
  status VARCHAR(50) DEFAULT 'PENDING',
  payment_method VARCHAR(50) NOT NULL,
  PRIMARY KEY (order_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (delivery_id) REFERENCES delivery_options(delivery_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO orders VALUES
(1,2,'2025-05-27 16:14:02',1,'123456789','shop 1356/2049 Logan Road','regular','regular','COMPLETED','PayPal'),
(2,3,'2025-05-27 16:14:41',2,'1235123623','694 Brunswick Street, New Farm','regular2','regular2','CANCELLED','Apple Pay'),
(3,4,'2025-05-27 16:15:29',3,'1235124623','P block 2 George Street, Brisbane City QLD 4000, Australia','regular3','regular3','PENDING','Credit/Debit Card');

CREATE TABLE order_items (
  order_item_id INT NOT NULL AUTO_INCREMENT,
  order_id INT,
  item_id INT,
  quantity INT NOT NULL,
  PRIMARY KEY (order_item_id),
  FOREIGN KEY (order_id) REFERENCES orders(order_id),
  FOREIGN KEY (item_id) REFERENCES items(item_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO order_items VALUES
(1,1,3,2),
(2,1,7,1),
(3,2,11,1),
(4,2,5,2),
(5,2,6,1),
(6,3,8,2);
