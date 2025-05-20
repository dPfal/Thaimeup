
from thaimeup.models import Order, OrderStatus, UserInfo, Item, BasketItem
from thaimeup.models import UserAccount
from datetime import datetime
from flask import Flask
from . import mysql

DummyUserInfo = []

dummy_item1 = Item(
    id="1",
    name="Burger",
    description="Juicy grilled beef burger",
    category="Food",
    price=9.99,
    is_available=True,
    image="padthai.jpeg"
)

dummy_item2 = Item(
    id="2",
    name="Fries",
    description="Crispy golden fries",
    category="Side",
    price=4.99,
    is_available=True,
    image="somtum.jpeg"
)

basket_item1 = BasketItem(id="b1", item=dummy_item1, quantity=2)
basket_item2 = BasketItem(id="b2", item=dummy_item2, quantity=3)

Orders = [

    ]


def get_items():
    """Get all items."""
    cur = mysql.connection.cursor()
    cur.execute("""
    SELECT items.item_id, items.name, items.description, categories.category_name, 
    items.price, items.image, items.is_available 
    FROM items 
    INNER JOIN categories ON items.category_id = categories.category_id
    """)
    results = cur.fetchall()
    cur.close()
    return [Item(str(row['item_id']), row['name'], row['description'], row['category_name'], 
            row['price'], bool(row['is_available']), row['image']) for row in results]


def get_item(item_id):
    """Get item data by its ID."""
    cur = mysql.connection.cursor()
    cur.execute("""
    SELECT items.item_id, items.name, items.description, categories.category_name, 
           items.price, items.image, items.is_available 
    FROM items 
    INNER JOIN categories ON items.category_id = categories.category_id 
    WHERE item_id = %s
    """, (item_id,))     
    row = cur.fetchone()
    cur.close()
    return Item(str(row['item_id']), row['name'], row['description'], row['category_name'],
                 row['price'], bool(row['is_available']), row['image']) if row else None

def add_order(order):
    """Add a new order."""
    Orders.append(order)

def get_orders():
    """Get all orders."""
    return Orders

def get_order(order_id):
    """Get an order by its ID."""
    order_id = str(order_id)
    for order in Orders:
        if order.id == order_id:
            return order
    return None  # or raise an exception if preferred

def mark_order_as_pending(order_id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE orders SET status = 0 WHERE order_id = %s", (order_id,))
    mysql.connection.commit()
    cur.close()

def mark_order_as_completed(order_id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE orders SET status = 1 WHERE order_id = %s", (order_id,))
    mysql.connection.commit()
    cur.close()  



def get_user_by_id(user_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT user_id, username, password_hash, email, first_name, last_name, phone
        FROM users
        WHERE user_id = %s
    """, (user_id,))
    row = cur.fetchone()
    cur.close()
    if row:
        return UserAccount(
            username=row['username'],
            password=row['password_hash'],
            email=row['email'],
            info=UserInfo(
                id=str(row['user_id']),
                firstname=row['first_name'],
                surname=row['last_name'],
                email=row['email'],
                phone=row['phone']
            )
        )
    return None


def check_for_user(username, password):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT user_id, username, password_hash, email, first_name, last_name, phone
        FROM users
        WHERE username = %s AND password_hash = %s
    """, (username, password))
    row = cur.fetchone()
    cur.close()
    if row:
        return UserAccount(row['username'], row['password_hash'], row['email'],
                           UserInfo(str(row['user_id']), row['first_name'], row['last_name'],
                                    row['email'],row['phone']))
    return None

def check_user_exists(username, email, phone):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT username, email, phone FROM users
        WHERE username = %s OR email = %s OR phone = %s
    """, (username, email, phone))
    
    exists = cur.fetchone() is not None 
    cur.close()
    return exists


def add_user(form):
    cur = mysql.connection.cursor()
    check_admin = is_admin(form.username.data)
    cur.execute(
        "INSERT INTO users(first_name, last_name, username, password_hash, email, is_admin, phone) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (
            form.firstname.data,
            form.surname.data,
            form.username.data,
            form.password.data,
            form.email.data,
            check_admin,
            form.phone.data
        )
    )
    mysql.connection.commit()
    cur.close()
    return True


def is_admin(username):
    return 'admin' in username.lower()

def get_categories():
    cur = mysql.connection.cursor()
    cur.execute("SELECT category_id, category_name FROM categories")
    categories = cur.fetchall()
    cur.close()
    return [(c['category_id'], c['category_name']) for c in categories]

def insert_item(name, description, price,image,category_id, is_available):
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO items (name, description, price,image, category_id, is_available)
        VALUES (%s, %s, %s, %s, %s,%s)
    """, (name, description, price,image, category_id, is_available))
    mysql.connection.commit()
    cur.close()

def update_item(item_id, new_name, new_description, new_price, new_category_id):
    print(f"[DB] Updating item {item_id}...")
    print(f"name={new_name}, price={new_price}, category={new_category_id}")
    
    cur = mysql.connection.cursor()
    sql = """
        UPDATE items
        SET name = %s,
            description = %s,
            price = %s,
            category_id = %s
        WHERE item_id = %s
    """
    cur.execute(sql, (new_name, new_description, new_price, new_category_id, item_id))
    mysql.connection.commit()
    cur.close()
    print("[DB] ✅ Commit complete")

def delete_item(item_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM items WHERE item_id = %s", (item_id,))
    mysql.connection.commit()
    cur.close()

def mark_item_as_available(item_id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE items SET is_available = 1 WHERE item_id = %s", (item_id,))
    mysql.connection.commit()
    cur.close()

def mark_item_as_unavailable(item_id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE items SET is_available = 0 WHERE item_id = %s", (item_id,))
    mysql.connection.commit()
    cur.close()    