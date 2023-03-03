from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound

from mock_data import ARTICLES, USERS

articles_app = Blueprint('articles_app', __name__, url_prefix='/articles', static_folder='../static')


@articles_app.route('/', endpoint='list')
def articles_list():
    return render_template('articles/list.html', articles=ARTICLES)


@articles_app.route('/<int:article_id>/', endpoint='details')
def user_details(article_id: int):
    try:
        article = ARTICLES[article_id]
        author = USERS[article['author']]
        title = article['title']
        body = article['body']
    except KeyError:
        raise NotFound(f"Article #{article_id} doesn't exist!")
    return render_template('articles/details.html',
                           author=author,
                           title=title,
                           body=body)
