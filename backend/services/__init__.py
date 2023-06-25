from flask import Flask
from dashboard.admin import admin
from config import db, cors, jwt
from config.Base import Config
from services.bet.view import bet
from services.client.view import auth
from services.mail import mail


def init_app(app):
    admin.init_app(app)
    cors.init_app(app, resources={r"*": {"origins": "*"}})
    mail.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()


def router_app(app):
    app.register_blueprint(auth)
    app.register_blueprint(bet)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    init_app(app)
    router_app(app)

    return app
