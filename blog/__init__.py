from flask import Flask
from flask_combo_jsonapi import Api

from blog.models.database import db, migrate

api = Api()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object('blog.config')

    db.init_app(app)
    app.app_context().push()
    migrate.init_app(app, db, compare_type=True)

    from blog.views.auth import login_manager
    login_manager.init_app(app)

    from flask_wtf import CSRFProtect
    csrf = CSRFProtect()
    csrf.init_app(app)

    from blog.admin import admin
    admin.init_app(app)

    register_blueprints(app)
    register_commands(app)

    from combojsonapi.spec import ApiSpecPlugin
    api.plugins = [
        ApiSpecPlugin(
            app=app,
            tags={
                'Tag': 'Tag API',
                'User': 'User API',
                'Author': 'Author API',
                'Article': 'Article API',
            }
        ),
    ]
    api.init_app(app)
    register_api_routes(api)

    return app


def register_blueprints(app: Flask):
    from blog.views.authors import authors_app
    from blog.views.index import index_app
    from blog.views.users import users_app
    from blog.views.articles import articles_app
    from blog.views.auth import auth_app

    app.register_blueprint(index_app)
    app.register_blueprint(users_app)
    app.register_blueprint(articles_app)
    app.register_blueprint(auth_app)
    app.register_blueprint(authors_app)


def register_commands(app: Flask):
    from blog import commands

    app.cli.add_command(commands.create_admin)
    app.cli.add_command(commands.create_tags)


def register_api_routes(api_):
    from blog.api.tag import TagList, TagDetail
    from blog.api.user import UserList, UserDetail
    from blog.api.author import AuthorList, AuthorDetail
    from blog.api.article import ArticleList, ArticleDetail

    api_.route(TagList, 'tag_list', '/api/tags/', tag='Tag')
    api_.route(TagDetail, 'tag_detail', '/api/tags/<int:id>/', tag='Tag')

    api_.route(UserList, 'user_list', '/api/users/', tag='User')
    api_.route(UserDetail, 'user_detail', '/api/users/<int:id>/', tag='User')

    api_.route(AuthorList, 'author_list', '/api/authors/', tag='Author')
    api_.route(
        AuthorDetail,
        'author_detail',
        '/api/authors/<int:id>/',
        tag='Author',
    )

    api_.route(ArticleList, 'articles_list', '/api/articles/', tag='Article')
    api_.route(
        ArticleDetail,
        'article_detail',
        '/api/articles/<int:id>/',
        tag='Article',
    )
