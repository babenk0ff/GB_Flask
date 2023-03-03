from flask import Blueprint, render_template

index_app = Blueprint('index_app', __name__, url_prefix='/')


@index_app.route('/', endpoint='index')
def index():
    return render_template('index.html')
