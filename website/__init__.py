from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db_name = "database.db"
db = SQLAlchemy()


def create_database(app):
    if not path.exists("website/" + db_name):
        db.create_all(app=app)
        print("Database created!")


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "SHBUBHSDK"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_name}"
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Note

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.signin"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
