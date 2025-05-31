from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from enum import Enum

@dataclass
class Item:
    id: str
    name: str
    description: str
    category: str  
    price: float
    is_available: bool
    image: str = 'foobar.png'
   
    
@dataclass
class UserInfo:
    id: str
    firstname: str
    surname: str
    email: str
    phone: str

@dataclass
class UserAccount:
    username: str
    password: str
    email: str
    info: UserInfo

@dataclass 
class BasketItem:
    id: str
    item: Item
    quantity: int

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
    
    def empty(self):
        """Empty the basket."""
        self.items = []
    
    def total_cost(self):
        """Calculate the total cost of the basket."""
        return sum(item.total_price() for item in self.items)

class OrderStatus(Enum):
    PENDING = 'PENDING'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'

    def is_pending(self):
        return self == OrderStatus.PENDING
    
    def is_completed(self):
        return self == OrderStatus.COMPLETED

@dataclass
class Order:
    id: str
    status: 'OrderStatus'
    user: 'UserInfo'
    items: List['BasketItem'] = field(default_factory=list)
    date: datetime = field(default_factory=datetime.now)

    delivery_method: str = 'Standard'     
    payment_method: str = 'Credit Card'  
    recipient_phone: str = ''
    recipient_address: str = ''
    recipient_first_name: str = ''
    recipient_last_name: str = ''
    delivery_fee: float = 0.0

    def calculate_total_cost(self) -> float:
        return sum(item.total_price() for item in self.items) + self.delivery_fee



