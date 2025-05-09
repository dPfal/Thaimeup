
from thaimeup.models import City, Tour, Order, OrderStatus, UserInfo, Item
from thaimeup.models import UserAccount
from datetime import datetime
from flask import Flask
from dotenv import load_dotenv
import os
import pymysql

load_dotenv()

def get_connection():
    connection = pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        port=int(os.getenv('DB_PORT')),
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

DummyCity = City('0', 'Dummy', 'Dummy city for testing', 'dummy.jpg')

Cities = [
    City('1', 'Sydney', 
        'City in New South Wales with largest population', 
        'sydney.jpg'),
    City('2', 'Brisbane', 
        'City in Queensland with a good weather', 
        'brisbane.jpg'),
    City('3', 'Melbourne',
        'Visit a city in Melbourne and experience all four seasons in a day!',
        'melbourne.jpg')
]

DummyItem = Item('0', 'Dummy', 'Dummy des', 'Dummy Allergy', '19', 'dummy.jpg')

Items = [
    Item('1', 'Pad Thai', 'Stir-fried rice noodles with tofu, shrimp, bean sprouts, peanuts, and tamarind sauce', 'None', '20.90', 'padthai.jpeg'),
    Item('2', 'Pad Se Ew', 'Fat rice noodle stir fried in soy and oyster sauce with Asian greens', 'None', '21.90', 'padseew.jpeg'),
    Item('3', 'Som Tum', 'Fresh shredded green papaya with chili, lime, fish sauce, tomatoes, and peanuts', 'None', '17.90', 'somtum.jpeg'),
    Item('4', 'Fried Rice', 'Fried jasmine rice with eggs, vegetables, and your choice of chicken, shrimp, or tofu', 'None', '19.00', 'friedrice.jpeg'),
    Item('5', 'Roti', 'Hot Roti', 'None', '3.00', 'roti.jpeg'),
    Item('6', 'Springrolls', 'Vegetable Springrolls (4pcs)', 'None', '12.50', 'springrolls.jpeg'),
    Item('7', 'Green Curry', 'Spicy green curry with chicken, eggplant, bamboo shoots, and basil in coconut milk', 'None', '23.00', 'greencurry.jpeg'),
    Item('8', 'Massaman Curry', 'Rich, mild curry made with beef, potatoes, peanuts, and a touch of cinnamon', 'None', '24.00', 'massaman.jpeg'),
    Item('9', 'Panang Curry', 'Thick, creamy red curry with beef or chicken, bell peppers, and kaffir lime leaves', 'None', '21.50', 'panang.jpeg'),
    Item('10', 'Thai Fish Cakes', 'Spicy fish patties with red curry paste and kaffir lime leaves, served with sweet chili sauce', 'None', '13.90', 'fishcake.jpeg'),
    Item('11', 'Tom Yum Soup', 'Hot and sour soup with shrimp, lemongrass, galangal, lime leaves, and chili', 'None', '19.50', 'tomyum.jpeg'),
    Item('12', 'Larb', 'Spicy minced chicken salad with lime juice, chili, mint, and roasted rice powder', 'None', '18.00', 'larb.jpeg'),
    Item('13', 'Mango Sticky Rice', 'Sweet sticky rice served with fresh mango and coconut cream', 'None', '14.00', 'mangosticky.jpeg'),
    Item('14', 'Pad Kee Mao', 'Spicy stir-fried rice noodles with chili, garlic, basil, and vegetables', 'None', '21.00', 'padkeemao.jpeg'),
    Item('15', 'Thai Satay', 'Grilled marinated chicken skewers served with peanut sauce and cucumber relish', 'None', '16.50', 'satay.jpeg')
]


DummyTour = Tour('0', 'Dummy Tour', 'Dummy tour for testing',
                 DummyCity, 'dummy.jpg', 25.25, datetime.now())

Tours = [
    Tour('1', 'Kangaroo point walk',
         'Gentle stroll but be careful of cliffs. Hand feed the kangaroos',
          Cities[1], 't_hand.jpg', 99.00, datetime(2023, 7, 23)),
    Tour('2', 'West End markets',
         'Tour the boutique goods and food and ride the wheel',
         Cities[1], 't_ride.jpg', 20.00,  datetime(2023, 10, 30)),
    Tour('3', 'Whale spotting',
         'Visit the incredible Sydney coast line and see the whales migrating',
         Cities[0], 't_whale.jpg', 129.00,  datetime(2023, 10, 30))
]

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

def get_cities():
    """Get all cities."""
    return Cities

def get_items():
    """Get all items."""
    return Items

def get_item(item_id):
    """Get an item by its ID."""
    item_id = str(item_id)
    for item in Items:
        if item.id == item_id:
            return item
    return DummyItem

def get_city(city_id):
    """Get a city by its ID."""
    city_id = str(city_id)
    for city in Cities:
        if city.id == city_id:
            return city
    return DummyCity

def get_tours():
    """Get all tours."""
    return Tours

def get_tour(tour_id):
    """Get a tour by its ID."""
    tour_id = str(tour_id)
    for tour in Tours:
        if tour.id == tour_id:
            return tour
    return DummyTour

def get_tours_for_city(city_id):
    """Get all tours for a given city ID."""
    city_id = str(city_id)
    return [tour for tour in Tours if tour.city.id == city_id]

def add_city(city):
    """Add a new city."""
    Cities.append(city)

def add_tour(tour):
    """Add a new tour."""
    Tours.append(tour)

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
