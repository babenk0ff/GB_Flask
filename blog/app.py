from flask import Flask

from blog.views.articles import articles_app
from blog.views.index import index_app
from blog.views.users import users_app


def create_app() -> Flask:
    app = Flask(__name__)
    register_blueprints(app)
    return app


def register_blueprints(app: Flask):
    app.register_blueprint(index_app)
    app.register_blueprint(users_app)
    app.register_blueprint(articles_app)
