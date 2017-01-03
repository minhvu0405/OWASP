from flask import Flask
from flaskext.mysql import MySQL
from flask.ext.login import LoginManager

mysql = MySQL()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'myPassword'
app.config['MYSQL_DATABASE_DB'] = 'myDatabase'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

from app import views