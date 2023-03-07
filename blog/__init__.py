from flask import Flask
from flask_wtf import CSRFProtect

from blog.views.articles import articles_app
from blog.views.auth import auth_app, login_manager
from blog.views.index import index_app
from blog.views.users import users_app

from blog.models.database import db, migrate
from blog import commands


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object('blog.config')

    db.init_app(app)
    migrate.init_app(app, db, compare_type=True)

    login_manager.init_app(app)

    csrf = CSRFProtect()
    csrf.init_app(app)

    register_blueprints(app)
    register_commands(app)
    return app


def register_blueprints(app: Flask):
    app.register_blueprint(index_app)
    app.register_blueprint(users_app)
    app.register_blueprint(articles_app)
    app.register_blueprint(auth_app)


def register_commands(app: Flask):
    app.cli.add_command(commands.create_admin)
