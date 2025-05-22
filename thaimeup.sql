DROP TABLE IF EXISTS order_items, orders, items, categories, delivery_options, users;

-- Categories table
CREATE TABLE categories (
  category_id INT NOT NULL AUTO_INCREMENT,
  category_name VARCHAR(50) NOT NULL,
  PRIMARY KEY (category_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO categories (category_id, category_name) VALUES
(1,'Rice'), (2,'Noodle'), (3,'Entree'), (4,'Salad'), (5,'Curry');

-- Delivery options table
CREATE TABLE delivery_options (
  delivery_id INT NOT NULL AUTO_INCREMENT,
  delivery_name VARCHAR(100) NOT NULL,
  cost DECIMAL(10,2) DEFAULT 0.00,
  PRIMARY KEY (delivery_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO delivery_options (delivery_id, delivery_name, cost) VALUES
(1,'Standard',5.00), (2,'Express',10.00), (3,'Eco',3.00);

-- Users table
CREATE TABLE users (
  user_id INT NOT NULL AUTO_INCREMENT,
  username VARCHAR(50) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  email VARCHAR(100) NOT NULL UNIQUE,
  first_name VARCHAR(50),
  last_name VARCHAR(50),
  is_admin TINYINT(1) DEFAULT 0,
  phone VARCHAR(20),
  PRIMARY KEY (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Items table
CREATE TABLE items (
  item_id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  description VARCHAR(255),
  price DECIMAL(10,2) NOT NULL,
  image VARCHAR(255),
  category_id INT,
  is_available TINYINT(1) DEFAULT 1,
  PRIMARY KEY (item_id),
  FOREIGN KEY (category_id) REFERENCES categories(category_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO items (item_id, name, description, price, image, category_id, is_available) VALUES
(1,'Pad Thai','Stir-fried rice noodles with tofu, shrimp, bean sprouts, peanuts, and tamarind sauce',20.90,'padthai.jpeg',2,0),
(2,'Pad Se Ew','Fat rice noodle stir fried in soy and oyster sauce with Asian greens',21.90,'padseew.jpeg',2,0),
(3,'Som Tum','Fresh shredded green papaya with chili, lime, fish sauce, tomatoes, and peanuts',17.90,'somtum.jpeg',4,1),
(4,'Fried Rice','Fried jasmine rice with eggs, vegetables, and your choice of chicken, shrimp, or tofu',19.00,'friedrice.jpeg',1,1),
(5,'Roti','Hot Roti',3.00,'roti.jpeg',3,1),
(6,'Springrolls','Vegetable Springrolls (4pcs)',12.50,'springrolls.jpeg',3,1),
(7,'Green Curry','Spicy green curry with chicken, eggplant, bamboo shoots, and basil in coconut milk',23.00,'greencurry.jpeg',5,1),
(8,'Massaman Curry','Rich, mild curry made with beef, potatoes, peanuts, and a touch of cinnamon',24.00,'massaman.jpeg',5,1),
(9,'Panang Curry','Thick, creamy red curry with beef or chicken, bell peppers, and kaffir lime leaves',21.50,'panang.jpeg',5,1),
(10,'Thai Fish Cakes','Spicy fish patties with red curry paste and kaffir lime leaves, served with sweet chili sauce',13.90,'fishcake.jpeg',3,1),
(11,'Tom Yum Soup','Hot and sour soup with shrimp, lemongrass, galangal, lime leaves, and chili',19.50,'tomyum.jpeg',3,1),
(12,'Larb','Spicy minced chicken salad with lime juice, chili, mint, and roasted rice powder',18.00,'larb.jpeg',4,1),
(13,'Mango Sticky Rice','Sweet sticky rice served with fresh mango and coconut cream',14.00,'mangosticky.jpeg',3,1),
(14,'Pad Kee Mao','Spicy stir-fried rice noodles with chili, garlic, basil, and vegetables',21.00,'padkeemao.jpeg',2,1),
(15,'Thai Satay','Grilled marinated chicken skewers served with peanut sauce and cucumber relish',16.50,'satay.jpeg',3,1);

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

CREATE TABLE order_items (
  order_item_id INT NOT NULL AUTO_INCREMENT,
  order_id INT,
  item_id INT,
  quantity INT NOT NULL,
  PRIMARY KEY (order_item_id),
  FOREIGN KEY (order_id) REFERENCES orders(order_id),
  FOREIGN KEY (item_id) REFERENCES items(item_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;