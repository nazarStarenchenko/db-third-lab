from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import psycopg2
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = 'secret key'
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:3220@localhost:5432/flask_db"
    db.init_app(app)

    from .views import  views
    from .auth import  auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    #uncomment this line and run the app if you want to create user and note 
    #tables at flask_db, that needs to be already created
    #db.create_all(app=app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

    