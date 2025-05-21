from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, StringField, PasswordField,SelectField,DecimalField,TextAreaField, RadioField
from wtforms.validators import InputRequired, email, NumberRange

class CheckoutForm(FlaskForm):
    """Form for user checkout."""
    firstname = StringField("First name", validators=[InputRequired()])
    surname = StringField("Last name", validators=[InputRequired()])
    phone = StringField("Phone Number", validators=[InputRequired()])
    address = StringField("Address", validators=[InputRequired()])

    delivery_method = RadioField("Delivery Method", choices=[
        ('1', 'Standard Delivery (+$5.00)'),
        ('2', 'Express Delivery (+$10.00)'),
        ('3', 'Eco Delivery (+$3.00)')
    ], default='1', validators=[InputRequired()])

    payment_method = RadioField("Payment Method", choices=[
        ('PayPal'),
        ('Apple Pay'),
        ('Credit/Debit Card')
    ], default='PayPal', validators=[InputRequired()])
    submit = SubmitField("Place Order")


class LoginForm(FlaskForm):
    """Form for user login."""
    username = StringField("Username", validators = [InputRequired()])
    password = PasswordField("Password", validators = [InputRequired()])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    """Form for user registry."""
    username = StringField("Username", validators = [InputRequired()])
    password = PasswordField("Password", validators = [InputRequired()])
    email = StringField("Email", validators = [InputRequired(), email()])
    firstname = StringField("Your first name", validators = [InputRequired()])
    surname = StringField("Your surname", validators = [InputRequired()])
    phone = StringField("Your phone number", validators = [InputRequired()])
    submit = SubmitField("Make Account")

class AddItemForm(FlaskForm):
    name = StringField("Menu Name", validators=[InputRequired()])
    description = TextAreaField("Description", validators=[InputRequired()])
    price = DecimalField("Price", validators=[InputRequired(), NumberRange(min=0)])
    category = SelectField("Category", coerce=int, validators=[InputRequired()])
    is_available = SelectField("Availability", choices=[('1', 'Available'), ('0', 'Sold Out')], validators=[InputRequired()])
    submit = SubmitField("Add Item")


class EditItemForm(FlaskForm):
    name = StringField("Menu Name", validators=[InputRequired()])
    description = TextAreaField("Description", validators=[InputRequired()])
    price = DecimalField("Price", places=2, validators=[InputRequired(), NumberRange(min=0)])
    category = SelectField("Category", coerce=int, validators=[InputRequired()])
    submit = SubmitField("Save Changes")