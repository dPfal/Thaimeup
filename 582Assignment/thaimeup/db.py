
from thaimeup.models import Order, OrderStatus, UserInfo, Item, BasketItem
from thaimeup.models import UserAccount
from datetime import datetime
from flask import Flask
from . import mysql

DummyUserInfo = UserInfo(
    '0', 'Dummy', 'Foobar', 'dummy@foobar.com', '1234567890'
)

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
    Order('1', OrderStatus.PENDING, DummyUserInfo, 149.99,
          [basket_item1, basket_item2]),  
    Order('2', OrderStatus.PENDING, DummyUserInfo, 1000.00,[basket_item1])
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