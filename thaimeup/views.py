from flask import Blueprint, render_template, request, session, flash
from flask import redirect, url_for,abort
from thaimeup import mysql
from thaimeup.db import  get_orders, check_for_user, add_user, is_admin, insert_order,update_order_status_in_db, get_all_categories, search_items, get_items_by_category, get_category_name
from thaimeup.db import get_items, get_item, update_item,mark_item_as_unavailable, mark_item_as_available,status_orders_for_item, mark_item_as_deleted, insert_category,insert_item,get_categories,mark_category_as_deleted
from thaimeup.session import get_basket, add_to_basket, empty_basket, get_user
from thaimeup.forms import CheckoutForm, LoginForm, RegisterForm,AddCategoryForm,AddItemForm,EditItemForm, DeleteCategoryForm
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



@bp.route('/itemdetails/<int:itemid>/', methods=['GET'])
def itemdetails(itemid):
    quantity = request.args.get('quantity', 1, type=int)
    action   = request.args.get('action')

    if action == 'decrease':
        if quantity <= 1:
            flash("The quantity must be at least 1", "error")
        else:
            quantity -= 1

    elif action == 'increase':
        if quantity >= 10:
            flash("The quantity must be at most 10", "error")
        else:
            quantity += 1

    quantity = max(1, min(quantity, 10))

    item = get_item(itemid)
    return render_template(
        'itemdetails.html',
        item=item,
        quantity=quantity
    )



@bp.route('/order/', methods = ['POST', 'GET'])
def order():
    item_id = request.args.get('item_id')
    if 'order_id'not in session:
        session['order_id'] = 1 
    
    order = get_basket()
    if item_id:
        add_to_basket(item_id, 1)

    return render_template('basket.html', order=order, totalprice=float(order.total_cost()))

@bp.route('/basket/<int:item_id>/', methods = ['POST', 'GET'])
def adding_to_basket(item_id):
    add_to_basket(item_id, 1)
    return redirect(url_for('main.order'))

@bp.route('/basket/<int:item_id>/<int:quantity>/', methods = ['POST', 'GET'])
def adding_to_basket_with_quantity(item_id, quantity):
    add_to_basket(item_id, quantity)
    return redirect(url_for('main.order'))

@bp.route('/clearbasket/', methods = ['POST', 'GET'])
def clear_basket():
    session['basket'] = {"items": []}
    return redirect(url_for('main.order'))

@bp.route('/removebasketitem/<int:item_id>/', methods = ['POST', 'GET'])
def remove_basketitem(item_id):
    basket_data = session.get('basket', {"items": []})
    basket_data["items"] = [item for item in basket_data["items"] if str(item["id"]) != str(item_id)]
    session["basket"] = basket_data
    session.modified = True 
    return redirect(url_for('main.order'))


@bp.route('/updatebasket/<int:item_id>/<string:action>/', methods = ['POST', 'GET'])
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


    return render_template(
        "checkout.html",
        form=form,
        basket=basket,
        show_errors=(request.method == 'POST'),
        product_total=basket.total_cost,
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




@bp.route('/admin/manage-categories/', methods=['GET', 'POST'])
@only_admins
def manage_categories():
    add_form = AddCategoryForm()
    delete_form = DeleteCategoryForm()
    delete_form.category_id.choices = get_categories()

    if add_form.validate_on_submit() and add_form.submit.data:
        name = add_form.category.data
        insert_category(name)
        flash("Category added successfully.")
        return redirect(url_for('main.manage_categories'))
    
    if delete_form.validate_on_submit() and delete_form.submit.data:
        category_id = delete_form.category_id.data
        category_name = get_category_name(category_id)

        active_items = get_items_by_category(category_name)
        if active_items:
            flash("This category is associated with menu products. Please edit those products in order to delete it.")
            return redirect(url_for('main.manage_categories'))
        
        mark_category_as_deleted(category_id)
        flash("Category deleted successfully.")
        return redirect(url_for('main.manage_categories'))
    

    return render_template('manage_categories_admin.html', add_form=add_form, delete_form=delete_form)




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

    elif request.method == 'GET':
        form.name.data = item.name
        form.description.data = item.description
        form.price.data = item.price
        form.category.data = item.category

    return render_template("edit_item_admin.html", form=form, item=item)

@bp.route('/admin/delete/<int:item_id>/', methods=['POST'])
@only_admins
def delete_menu(item_id):
    statuses = status_orders_for_item(item_id)

    if statuses and any(status not in ['COMPLETED', 'CANCELLED'] for status in statuses):
        flash("This item is part of pending order(s). Please complete or cancel the order(s) to remove it.")
    else:
        mark_item_as_deleted(item_id)
        flash("Item deleted.")
    return redirect(url_for('main.index', item_id=item_id))

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
