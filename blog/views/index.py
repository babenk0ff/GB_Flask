from flask import Blueprint, redirect, url_for

index_app = Blueprint('index_app', __name__, url_prefix='/')


@index_app.route('/', endpoint='index')
def index():
    return redirect(url_for('articles_app.list'))
