from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, StringField, PasswordField,SelectField,DecimalField,TextAreaField, RadioField
from wtforms.validators import InputRequired, email, NumberRange,EqualTo
from thaimeup.db import is_username_taken,is_phone_taken,is_email_taken,is_category_taken
from wtforms import ValidationError

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

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, Email, Regexp

class RegisterForm(FlaskForm):
    """Form for user registration."""

    username = StringField(
        "Username",
        validators=[
            InputRequired(),
            Length(min=4, max=20, message="Username must be between 4 and 20 characters.")
        ]
    )
    def validate_username(self, field):
        if is_username_taken(field.data):
            raise ValidationError("This username is already taken.")    

    email = StringField(
        "Email",
        validators=[
            InputRequired(),
            Email(message="Please enter a valid email address.")
        ]
    )
    def validate_email(self, field):
        if is_email_taken(field.data):
            raise ValidationError("This email is already registered.")

    phone = StringField(
        "Phone Number",
        validators=[
            InputRequired(),
            Regexp(r'^\d{9,15}$', message="Enter a valid phone number (9–15 digits).")
        ]
    )
    def validate_phone(self, field):
        if is_phone_taken(field.data):
            raise ValidationError("This phone number is already registered.")

    password = PasswordField("Password", validators=[
        InputRequired(), Length(min=6),
        EqualTo('confirm_password', message="Passwords must match.")
    ])

    confirm_password = PasswordField("Confirm Password", validators=[
        InputRequired()
    ])

    firstname = StringField(
        "First Name",
        validators=[
            InputRequired(),
            Length(max=30, message="First name must be under 30 characters.")
        ]
    )

    surname = StringField(
        "Surname",
        validators=[
            InputRequired(),
            Length(max=30, message="Surname must be under 30 characters.")
        ]
    )

    submit = SubmitField("Create Account")


class AddCategoryForm(FlaskForm):
    category = StringField("Category Name", validators=[InputRequired()])

    def validate_category(self, field):
        category_name = field.data.strip().lower()
        if is_category_taken(category_name):
            raise ValidationError("This category already exists.")  

    submit = SubmitField("Add Category")

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