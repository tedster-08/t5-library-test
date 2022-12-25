from flask import Flask, render_template
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "troop5maplewoodnj"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    from .views import views

    app.register_blueprint(views, url_prefix="/")

    from . import models
    create_database(app)

    @app.errorhandler(404)
    def error404(e):
        return render_template("404.html", page_title="404", user=current_user), 404

    return app


def create_database(app):
    # if not os.path.exists('website/' + DB_NAME):
    db.create_all(app=app)
    print('Database created.')
