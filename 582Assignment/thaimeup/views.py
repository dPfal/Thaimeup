from flask import Blueprint, render_template, request, session, flash
from flask import redirect, url_for,abort
from thaimeup import mysql
from thaimeup.db import  get_orders, check_for_user, add_user, is_admin, insert_order,update_order_status_in_db, get_all_categories, search_items, get_items_by_category
from thaimeup.db import get_items, get_item, update_item,mark_item_as_unavailable, mark_item_as_available, delete_item,insert_category,insert_item,get_categories
from thaimeup.session import get_basket, add_to_basket, empty_basket, get_user
from thaimeup.forms import CheckoutForm, LoginForm, RegisterForm,AddCategoryForm,AddItemForm,EditItemForm
from thaimeup.models import UserAccount,UserInfo, BasketItem, Basket, Order, OrderStatus
from hashlib import sha256
from thaimeup.wrappers import only_admins

bp = Blueprint('main', __name__)


@bp.route('/', methods=['GET'])
def index():
    category = request.args.get('category', 'all')
    search = request.args.get('search', '').strip()
    categories = get_all_categories()

    if search:
        items = search_items(search)
    elif category == 'all':
        items = get_items()
    else:
        items = get_items_by_category(category)

    return render_template('index.html', items=items, categories=categories, category=category, search=search)



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

    return render_template('basket.html', order=order, totalprice=float(order.total_cost()))

@bp.post('/basket/<int:item_id>/')
def adding_to_basket(item_id):
    add_to_basket(item_id, 1)
    print(get_basket())
    return redirect(url_for('main.order'))

@bp.post('/basket/<int:item_id>/<int:quantity>/')
def adding_to_basket_with_quantity(item_id, quantity):
    add_to_basket(item_id, quantity)
    return redirect(url_for('main.order'))

@bp.post('/clearbasket/')
def clear_basket():
    print('User wants to clear the basket')
    session['basket'] = {"items": []}
    print(get_basket())
    return redirect(url_for('main.order'))

@bp.post('/removebasketitem/<int:item_id>/')
def remove_basketitem(item_id):
    print(f'User wants to delete basket item with id={item_id}')
    basket_data = session.get('basket', {"items": []})
    basket_data["items"] = [item for item in basket_data["items"] if str(item["id"]) != str(item_id)]
    session["basket"] = basket_data
    session.modified = True 
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

@bp.route('/admin/orders/')
@only_admins
def orders():
    orders = get_orders()
    return render_template('orders.html', orders = orders)

@bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if not session.get('logged_in'):
        flash("Please log in.")
        return redirect(url_for('main.login'))

    form = CheckoutForm()

    if request.method == 'POST' and form.validate_on_submit():
        return place_order(form)

    if request.method == 'GET':
        user = get_user()
        form.firstname.data = user.get('firstname', '')
        form.surname.data = user.get('surname', '')
        form.phone.data = user.get('phone', '')

    basket = get_basket()


    delivery_fees = {
        'standard': 5,
        'express': 15,
        'eco': 0
    }

    total_prices = {
        option: float(basket.total_cost())+ fee
        for option, fee in delivery_fees.items()
    }

    return render_template(
        "checkout.html",
        form=form,
        basket=basket,
        show_errors=(request.method == 'POST'),
        product_total=basket.total_cost,
        total_prices=total_prices
    )

@bp.route('/placeorder', methods=['GET', 'POST'])
def place_order(form):
    basket = get_basket()
    user = get_user()

    if not basket.items:
        flash("Your basket is empty.", "error")
        return redirect(url_for('main.order'))

    order = Order(
        id=None,
        status=OrderStatus.PENDING,
        user=user,
        items=basket.items
    )

    order_id = insert_order(order, form)

    empty_basket()

    flash(f"Thank you, {user['firstname']}! Your order #{order_id} has been placed.")
    return redirect(url_for('main.index'))




@bp.route('/login/', methods=['POST', 'GET'])
def login():
    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            form.password.data = sha256(form.password.data.encode()).hexdigest()
            user = check_for_user(form.username.data, form.password.data)
            if not user:
                flash('Invalid username or password', 'error')
                return redirect(url_for('main.login'))

            session['user'] = {
                'user_id': user.info.id,
                'firstname': user.info.firstname,
                'surname': user.info.surname,
                'email': user.info.email,
                'phone': user.info.phone,
                'is_admin': is_admin(user.username),
            }
            session['is_admin'] = is_admin(user.username)
            session['logged_in'] = True
            flash('Login successful!')
            return redirect(url_for('main.index'))

    return render_template('login.html', form=form)

@bp.route('/logout/')
def logout():
    """Clear session and show logout confirmation."""
    session.clear()
    flash('You have been logged out.', 'success')
    
    return render_template('logout.html')

@bp.route('/register/', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            form.password.data = sha256(form.password.data.encode()).hexdigest()
            add_user(form)
            flash('Registration successful!')
            return redirect(url_for('main.login'))

    return render_template('register.html', form=form)




@bp.route('/admin/add-category/', methods=['GET', 'POST'])
@only_admins
def add_category():
    form = AddCategoryForm()

    if form.validate_on_submit():
        name = form.category.data
        insert_category(name)
        flash("Category added successfully.")
        return redirect(url_for('main.index'))

    return render_template('add_category_admin.html', form=form)



@bp.route('/admin/add/', methods=['GET', 'POST'])
@only_admins
def add_item():
    form = AddItemForm()
    form.category.choices = get_categories()

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        price = float(form.price.data)
        category_id = form.category.data
        is_available = int(form.is_available.data)
        image = name.lower().replace(" ", "") + ".jpeg"
        insert_item(name, description, price,image, category_id, is_available)
        flash("Item added successfully.")
        return redirect(url_for('main.index'))

    return render_template('add_item_admin.html', form=form)



@bp.route('/admin/edit/<int:item_id>/', methods=['GET', 'POST'])
@only_admins
def edit_menu(item_id):
    item = get_item(item_id)
    if not item:
        abort(404)

    form = EditItemForm()
    form.category.choices = get_categories()

    if request.method == 'POST':
        if form.validate_on_submit():
            update_item(
                item_id,
                form.name.data,
                form.description.data,
                float(form.price.data),
                form.category.data
                )
            flash("Menu updated.")
            return redirect(url_for("main.edit_menu", item_id=item_id))
        else:
            flash("Fail.")
            print(form.errors)

    elif request.method == 'GET':
        form.name.data = item.name
        form.description.data = item.description
        form.price.data = item.price
        form.category.data = item.category

    return render_template("edit_item_admin.html", form=form, item=item)

@bp.route('/admin/delete/<int:item_id>/', methods=['POST'])
@only_admins
def delete_menu(item_id):
    delete_item(item_id)
    flash('Item deleted.')
    return redirect(url_for('main.index'))

@bp.route('/admin/unavailable/<int:item_id>/', methods=['POST'])
@only_admins
def mark_unavailable(item_id):
    mark_item_as_unavailable(item_id)
    flash('Item marked as sold out.')
    return redirect(url_for('main.edit_menu', item_id=item_id))

@bp.route('/admin/available/<int:item_id>/', methods=['POST'])
@only_admins
def mark_available(item_id):
    mark_item_as_available(item_id)
    flash('Item is now available for sale.')
    return redirect(url_for('main.edit_menu', item_id=item_id))

@bp.route('/admin/update_order_status/<int:order_id>', methods=['POST'])
@only_admins
def update_order_status(order_id):
    new_status = request.form.get('new_status')
    if new_status not in ['pending', 'completed', 'cancelled']:
        flash('Invalid status.', 'error')
        return redirect(url_for('main.orders'))

    update_order_status_in_db(order_id, new_status)

    flash(f"Order #{order_id} status updated to {new_status.capitalize()}.")
    return redirect(url_for('main.orders'))
    

    
@bp.route('/trigger-500')
def trigger_500():
    raise RuntimeError("Error")
