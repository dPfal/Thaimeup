from thaimeup.db import get_item
from thaimeup.models import Basket, BasketItem
from thaimeup.models import UserInfo, Order, OrderStatus

from flask import session

def get_user():
    return session.get('user')

def get_basket():
    basket_data = session.get('basket', {})
    tmp = Basket()
    for item in basket_data.get('items', []):
        tmp.add_item_basket(
            BasketItem(item['id'], get_item(item.get('item_id')), item.get('quantity', 1))
        )
    return tmp

def add_to_basket(item_id, quantity=1):
    session.setdefault('basket', {"items": []})
    basket = get_basket()
    item_obj = get_item(item_id)

    for item in basket.items:
        print(" - item.item:", item.item, "| item.id:", getattr(item.item, 'id', 'N/A'))

    found = False
    for item in basket.items:
        if item.item.id == item_obj.id:  
            item.quantity += quantity
            found = True
            break

    if not found:
        new_item = BasketItem(item_id, item_obj, quantity)
        basket.add_item_basket(new_item)

    session['basket'] = {
        "items": [
            {
                "id": i.id,
                "item_id": i.item.id,
                "quantity": i.quantity
            }
            for i in basket.items
        ]
    }


def empty_basket():
    session['basket'] = {"items": []}
