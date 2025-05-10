from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from enum import Enum

class OldCity:
    def __init__(self, id, name, description, image):
        self.id = id
        self.name = name
        self.description = description
        self.image = image

    def get_city_details(self):
        return str(self)

    def __repr__(self):
        str = "ID: {}, Name: {}, Description: {}, Image: {} \n" 
        str = str.format( self.id, self.name, self.description, self.image)
        return str

# we can save ourselves some time by using the dataclass decorator
# to create the class and its methods
# this will create the __init__ and __repr__ methods for us
# and we can add our own methods as needed
@dataclass
class City:
    id: str
    name: str
    description: str = 'fooobar'
    image: str = 'foobar.png'

class Item:
    id: str
    name: str
    description: str
    price: float
    image: str = 'foobar.png'

    def __init__(self, id, name, description, price, image):
        self.id = id
        self.name = name
        self.description = description
        self.price = float(price)
        self.image = image

class OrderStatus(Enum):
    PENDING = 'Pending'
    CONFIRMED = 'Confirmed'
    CANCELLED = 'Cancelled'

@dataclass
class UserInfo:
    id: str
    firstname: str
    surname: str
    email: str
    phone: str

@dataclass 
class BasketItem:
    id: str
    item: Item
    quantity: int = 1

    def total_price(self):
        """Calculate the total price for this basket item."""
        return float(self.item.price * self.quantity)
    
    def increment_quantity(self):
        """Increment the quantity of this basket item."""
        self.quantity += 1

    def decrement_quantity(self):
        """Decrement the quantity of this basket item."""
        if self.quantity > 1:
            self.quantity -= 1

@dataclass
class Basket:
    items: List[BasketItem] = field(
        default_factory=lambda: [])

    def add_item_basket(self, item: BasketItem):
        """Add item to the basket."""
        self.items.append(item)

    def remove_item_basket(self, item: BasketItem):
        """Remove item from the basket by its ID."""
        self.items = [i for i in self.items if i.id != item.id]

    def get_item_basket(self, item_id: str):
        """Get item from the basket by its ID."""
        for i in self.items:
            if i.id == item_id:
                return i
    
    def empty(self):
        """Empty the basket."""
        self.items = []
    
    def total_cost(self):
        """Calculate the total cost of the basket."""
        return sum(item.total_price() for item in self.items)


@dataclass
class Order:
    id: str
    status: OrderStatus
    user: UserInfo
    total_cost: float = 0.0
    items: List[BasketItem] = field(
        default_factory=list,
        init=True)
    date: datetime = field(
        default_factory=lambda: datetime.now(),
        init=True)
    

@dataclass
class UserAccount:
    username: str
    password: str
    email: str
    info: UserInfo