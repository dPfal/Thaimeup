
from thaimeup.models import Order, OrderStatus, UserInfo, Item, BasketItem
from thaimeup.models import UserAccount
from flask_mysqldb import MySQL

mysql = MySQL()


def get_items():
    """Get all items."""
    cur = mysql.connection.cursor()
    cur.execute("""
    SELECT items.item_id, items.name, items.description, categories.category_name, 
    items.price, items.image, items.is_available 
    FROM items 
    INNER JOIN categories ON items.category_id = categories.category_id
    WHERE items.is_deleted = 0
    """)
    results = cur.fetchall()
    cur.close()
    return [Item(str(row['item_id']), row['name'], row['description'], row['category_name'], 
            row['price'], bool(row['is_available']), row['image']) for row in results]


def get_all_categories():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT DISTINCT category_name 
        FROM categories
        WHERE is_deleted = 0
    """)
    rows = cur.fetchall()
    cur.close()
    return [row['category_name'] for row in rows]

def get_items_by_category(category_name):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT items.item_id, items.name, items.description, categories.category_name, 
               items.price, items.image, items.is_available 
        FROM items 
        INNER JOIN categories ON items.category_id = categories.category_id 
        WHERE categories.category_name = %s AND items.is_deleted = 0
    """, (category_name,))
    rows = cur.fetchall()
    cur.close()
    return [
        Item(
            str(row['item_id']), row['name'], row['description'],
            row['category_name'], row['price'], bool(row['is_available']),
            row['image']
        )
        for row in rows
    ]

def search_items(search):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT items.item_id, items.name, items.description, categories.category_name,
               items.price, items.image, items.is_available
        FROM items
        INNER JOIN categories ON items.category_id = categories.category_id
        WHERE items.name LIKE %s OR categories.category_name LIKE %s
    """, ('%' + search + '%', '%' + search + '%'))
    rows = cur.fetchall()
    cur.close()
    return [Item(str(row['item_id']), row['name'], row['description'], row['category_name'],
                 row['price'], bool(row['is_available']), row['image']) for row in rows]


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


def get_orders():
    cur = mysql.connection.cursor()
    cur.execute("""
    SELECT o.*, u.first_name, u.last_name, u.phone, d.delivery_name, d.cost
    FROM orders o
    JOIN users u ON o.user_id = u.user_id
    JOIN delivery_options d ON o.delivery_id = d.delivery_id
    ORDER BY o.status desc, o.order_date_time DESC
""")
    order_rows = cur.fetchall()

    orders = []
    for row in order_rows:
        user_info = UserInfo(
            id=row['user_id'],
            firstname=row['first_name'],
            surname=row['last_name'],
            email='',  
            phone=row['phone']
        )

        cur.execute("""
            SELECT oi.*, i.name, i.description, i.price, i.image, c.category_name
            FROM order_items oi
            JOIN items i ON oi.item_id = i.item_id
            JOIN categories c ON i.category_id = c.category_id
            WHERE oi.order_id = %s
        """, (row['order_id'],))
        item_rows = cur.fetchall()

        basket_items = []
        for item in item_rows:
            item_obj = Item(
                id=str(item['item_id']),
                name=item['name'],
                description=item['description'],
                category=item['category_name'],
                price=float(item['price']),
                is_available=True,
                image=item['image']
            )
            basket_items.append(BasketItem(
                id=str(item['order_item_id']),
                item=item_obj,
                quantity=item['quantity']
            ))

        order = Order(
            id=str(row['order_id']),
            status=OrderStatus(row['status'].upper()), 
            user=user_info,
            items=basket_items,
            date=row['order_date_time'],    
            delivery_method=row['delivery_name'],
            delivery_fee=float(row['cost']),
            payment_method=row['payment_method'],
            recipient_phone=row['recipient_phone'],
            recipient_address=row['recipient_address'],
            recipient_first_name=row['recipient_first_name'],
            recipient_last_name=row['recipient_last_name']
        )
        orders.append(order)

    cur.close()
    return orders



def get_order(order_id):
    conn = mysql.connection
    cur = conn.cursor()

    cur.execute("SELECT * FROM orders WHERE order_id = %s", (order_id,))
    order = cur.fetchone()

    cur.close()
    return order

def insert_order(order, form):
    conn = mysql.connection
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO orders (
            user_id, order_date_time, delivery_id,
            recipient_phone, recipient_address,
            recipient_first_name, recipient_last_name,
            payment_method, status
        ) VALUES (%s, NOW(), %s, %s, %s, %s, %s, %s, %s)
    """, (
        order.user['user_id'],
        form.delivery_method.data,
        form.phone.data,
        form.address.data,
        form.firstname.data,
        form.surname.data,
        form.payment_method.data, 
        'PENDING'
    ))
    order_id = cur.lastrowid

    for item in order.items:
        cur.execute("""
            INSERT INTO order_items (order_id, item_id, quantity)
            VALUES (%s, %s, %s)
        """, (
            order_id,
            item.item.id,
            item.quantity
        ))

    conn.commit()
    cur.close()
    return order_id







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
    cur.execute("""
        SELECT category_id, category_name 
        FROM categories
        WHERE is_deleted = 0
    """)
    categories = cur.fetchall()
    cur.close()
    return [(c['category_id'], c['category_name']) for c in categories]

def get_category_name(category_id):
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT category_name FROM categories WHERE category_id = %s",
        (category_id,)
    )
    row = cur.fetchone()
    cur.close()
    return row['category_name'] if row else None

def get_category_id(category_name):
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT category_id FROM categories WHERE category_name = %s",
        (category_name,)
    )
    row = cur.fetchone()
    cur.close()
    return row['category_id'] if row else None

def insert_category(category_name,):
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO categories (category_name)
        VALUES (%s)
    """, (category_name,))
    mysql.connection.commit()
    cur.close()

def is_category_taken(category_name):
    conn = mysql.connection
    with conn.cursor() as cursor:
        cursor.execute("SELECT 1 FROM categories WHERE category_name = %s", (category_name,))
        return cursor.fetchone() is not None   

def insert_item(name, description, price,image,category_id, is_available):
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO items (name, description, price,image, category_id, is_available)
        VALUES (%s, %s, %s, %s, %s,%s)
    """, (name, description, price,image, category_id, is_available))
    mysql.connection.commit()
    cur.close()

def update_item(item_id, new_name, new_description, new_price, new_category_id):
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

def mark_item_as_deleted(item_id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE items SET is_deleted = 1 WHERE item_id = %s", (item_id,))
    mysql.connection.commit()
    cur.close()

def mark_category_as_deleted(category_id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE categories SET is_deleted = 1 WHERE category_id = %s", (category_id,))
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

def update_order_status_in_db(order_id: int, new_status: str):
    """Update the status of a specific order in the database"""
    conn = mysql.connection
    cur = conn.cursor()
    new_status = new_status.upper() 
    cur.execute("UPDATE orders SET status = %s WHERE order_id = %s", (new_status, order_id))
    conn.commit()
    cur.close()    


def status_orders_for_item(item_id):
    """Order statuses that include the item to be removed"""
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT DISTINCT o.status
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.order_id
        WHERE oi.item_id = %s
    """, (item_id,))
    rows = cur.fetchall()
    cur.close()
    return [row['status'] for row in rows]

def is_username_taken(username):
    conn = mysql.connection
    with conn.cursor() as cursor:
        cursor.execute("SELECT 1 FROM users WHERE username = %s", (username,))
        return cursor.fetchone() is not None
    
def is_email_taken(email):
    conn = mysql.connection
    with conn.cursor() as cursor:
        cursor.execute("SELECT 1 FROM users WHERE email = %s", (email,))
        return cursor.fetchone() is not None

def is_phone_taken(phone):
    conn = mysql.connection
    with conn.cursor() as cursor:
        cursor.execute("SELECT 1 FROM users WHERE phone = %s", (phone,))
        return cursor.fetchone() is not None
    
