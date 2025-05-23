from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

mysql = MySQL()

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.debug = False

    app.secret_key = os.getenv("SECRET_KEY")

    app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
    app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
    app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
    app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
    app.config['MYSQL_PORT'] = int(os.getenv('MYSQL_PORT', 3306))
    app.config['MYSQL_CURSORCLASS'] = os.getenv('MYSQL_CURSORCLASS', 'DictCursor')

    mysql.init_app(app)
    
    Bootstrap5(app)

    from . import views
    app.register_blueprint(views.bp)

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html")

    @app.errorhandler(500)
    def internal_error(e):
        return render_template("500.html")

    from . import session
    return app

