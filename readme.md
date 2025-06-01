# Project Overview

ThaimeUp is a thai food ordering platform designed for users to browse and order food items from the restaurant. 
It includes both customer and admin functionalities with soft-delete capabilities and error page simulation for testing.

# Libraries to Install

Make sure to install the required libraries using the requirements.txt file

Run the following commands before attempting to run this code.
```bash
py -m pip install -r requirements.txt
python3 -m pip install -r requirements.txt
```

# Error page

The Offers and Contact Us pages are purposely designed to show 404 and 500 error pages.
These are intentional and do not represent actual code issues or real errors.

# Users

There are 4 regular users and 2 admin users.
The password for all these pre-populated users is '123456'.

# Database

Please create the database using the query in thaimeup.sql
and update the database password to your own in the __init__.py file before running the code.

# Delete items and categories scenario

We implemented soft delete functionality by adding a column named is_deleted to the items and categories tables.
The main purpose of this is to ensure that items still appear on the orders page even if they are deleted after an order has been completed or canceled.
However, on the landing page, users will not be able to see any items that are marked as deleted.

