
from thaimeup.models import Order, OrderStatus, UserInfo, Item
from thaimeup.models import UserAccount
from datetime import datetime
from flask import Flask
from . import mysql

DummyUserInfo = UserInfo(
    '0', 'Dummy', 'Foobar', 'dummy@foobar.com', '1234567890'
)

Orders = [
    Order('1', OrderStatus.PENDING, DummyUserInfo, 149.99,
          []),  
    Order('2', OrderStatus.CONFIRMED, DummyUserInfo, 1000.00,
          []) 
]

Users = [
    UserAccount('admin', 'admin', 'foobar@mail.com', 
                UserInfo('1', 'Admin', 'User', 'foobar@mail.com', 
                         '1234567890')
    ),
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
    return Item(str(row['item_id']), row['name'], row['description'], row['category_name'], row['price'], bool(row['is_available']), row['image']) if row else None

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
    return None  # or raise an exception if preferred

def get_user_by_id(user_id):
    """Find a UserAccount by user_id."""
    for user in Users:
        if user.info.id == str(user_id): 
            return user
    return None

def check_for_user(username, password):
    """Check if the username and password are valid."""
    for user in Users:
        # never store passwords in plain text in production code
        # this is just for demonstration purposes
        if user.username == username and user.password == password:
            return user
    return None  # or raise an exception if preferred

def add_user(form):
    """Add a new user."""
    Users.append(
        UserAccount(form.username.data, form.password.data, form.email.data,
            UserInfo(f'U{len(Users)}', 
                     form.firstname.data, form.surname.data , 
                     form.email.data, form.phone.data
                    )
        )
    )

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

def update_item(item_id, new_name, new_description, new_price):
    cur = mysql.connection.cursor()
    sql = """
        UPDATE items
        SET name = %s, description = %s, price=%s
        WHERE item_id = %s
    """
    cur.execute(sql, (new_name, new_description, new_price, item_id,))
    mysql.connection.commit()
    cur.close()

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