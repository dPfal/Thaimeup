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