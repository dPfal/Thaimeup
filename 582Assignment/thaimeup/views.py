from flask import Blueprint, render_template, request, session, flash
from flask import redirect, url_for

from thaimeup.db import add_order, get_orders, check_for_user, add_user
from thaimeup.db import get_items, get_item
from thaimeup.session import get_basket, add_to_basket, empty_basket, convert_basket_to_order
from thaimeup.forms import CheckoutForm, LoginForm, RegisterForm

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('index.html', items = get_items())

@bp.route('/itemdetails/<int:itemid>/')
def itemdetails(itemid):
    return render_template('itemdetails.html', item = get_item(itemid))


@bp.route('/order/', methods = ['POST', 'GET'])
def order():
    item_id = request.args.get('item_id')
    # is this a new order?
    if 'order_id'not in session:
        session['order_id'] = 1 # arbitry, we could set either order 1 or order 2
    
    #retrieve correct order object
    order = get_basket()
    # are we adding an item? - will be implemented later with DB
    if item_id:
        add_to_basket(item_id, 1)
        print('Added item_id={} to basket.'.format(item_id))

    return render_template('order.html', order=order, totalprice=float(order.total_cost()))

@bp.post('/basket/<int:item_id>/')
def adding_to_basket(item_id):
    add_to_basket(item_id, 1)
    return redirect(url_for('main.order'))

@bp.post('/basket/<int:item_id>/<int:quantity>/')
def adding_to_basket_with_quantity(item_id, quantity):
    add_to_basket(item_id, quantity)
    return redirect(url_for('main.order'))

@bp.post('/clearbasket/')
def clear_basket():
    print('User wants to clear the basket')
    session['basket'] = {"items": []}
    return redirect(url_for('main.order'))

@bp.post('/removebasketitem/<int:item_id>/')
def remove_basketitem(item_id):
    print('User wants to delete basket item with id={}'.format(item_id))
        # Retrieve the current basket data
    basket_data = session.get('basket', {"items": []})

    # Remove the item from the basket
    basket_data["items"] = [item for item in basket_data["items"] if item["id"] != item_id]

    # Update the session with the modified basket
    session['basket'] = basket_data
    return redirect(url_for('main.order'))

@bp.post('/updatebasket/<int:item_id>/<string:action>/')
def update_basket_quantity(item_id, action):
    item_to_remove = None
    basket = get_basket()
    for item in basket.items:
        if item.id == item_id:
            if action == 'increase':
                item.increment_quantity()
            elif action == 'decrease':
                if item.quantity > 1:
                    item.decrement_quantity()
                else:
                    item_to_remove = item 
            break

    if item_to_remove:
        basket.remove_item_basket(item_to_remove)

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
    return redirect(url_for('main.order'))

@bp.route('/checkout/', methods = ['POST', 'GET'])
def checkout():
    form = CheckoutForm() 
    if request.method == 'POST':
        
        #retrieve correct order object
        order = get_basket()
       
        if form.validate_on_submit():
            order.status = True
            order.firstname = form.firstname.data
            order.surname = form.surname.data
            order.email = form.email.data
            order.phone = form.phone.data
            order.address = form.address.data
            flash('Thank you for your information, your order is being processed!',)
            order = convert_basket_to_order(get_basket())
            empty_basket()
            add_order(order)
            print('Number of orders in db: {}'.format(len(get_orders())))
            return redirect(url_for('main.index'))
        else:
            flash('The provided information is missing or incorrect. Please complete the fields correctly to process your order.',
                  'error')

    return render_template('checkout.html', form = form)


@bp.route('/login/', methods = ['POST', 'GET'])
def login():
    form = LoginForm()
    if request.method == 'POST':

        if form.validate_on_submit():

            # Check if the user exists in the database
            user = check_for_user(
                form.username.data, form.password.data
            )
            if not user:
                flash('Invalid username or password', 'error')
                return redirect(url_for('main.login'))

            # Store user information in the session
            session['username'] = user.username
            session['logged_in'] = True
            flash('Login successful!')
            return redirect(url_for('main.index'))

    return render_template('login.html', form = form)

@bp.route('/logout/')
def logout():
    """Clear session and show logout confirmation."""
    session.clear()
    flash('You have been logged out.', 'success')
    
    return render_template('logout.html')

@bp.route('/register/', methods = ['POST', 'GET'])
def register():
    form = RegisterForm()
    if request.method == 'POST':

        if form.validate_on_submit():

            # Check if the user already exists
            user = check_for_user(
                form.username.data, form.password.data
            )
            if user:
                flash('User already exists', 'error')
                return redirect(url_for('main.register'))

            # Store user information in the database
            add_user(
                form
            )
            flash('Registration successful!')
            return redirect(url_for('main.login'))

    return render_template('register.html', form = form)
