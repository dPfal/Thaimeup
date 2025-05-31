from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_mysqldb import MySQL
from . import views

mysql = MySQL()

def create_app():
    app = Flask(__name__)
    app.debug = False

    app.secret_key = 'BetterSecretNeeded123'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = '12345678'
    app.config['MYSQL_DB'] = 'thaimeup'
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

    mysql.init_app(app)
    
    Bootstrap5(app)

    app.register_blueprint(views.bp)

    @app.errorhandler(404)
    def not_found(e):
        return  render_template("404.html"), 404

    @app.errorhandler(500)
    def internal_error(e):
        return render_template("500.html"), 500

    return app

