from flask import Blueprint, render_template, request, current_app, redirect, \
    url_for
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from werkzeug.exceptions import NotFound, abort

from blog.models.database import db
from blog.models import Author, Article, Tag, User
from blog.forms.article import CreateArticleForm, EditArticleForm

articles_app = Blueprint(
    'articles_app',
    __name__,
    url_prefix='/articles',
    static_folder='../static',
)


@articles_app.route('/', endpoint='list')
def articles_list():
    tag_name = request.args.get('tag')
    author_name = request.args.get('author_name')
    if tag_name:
        articles = Article.query.filter(Article.tags.any(name=tag_name))
    elif author_name:
        articles = (db.session.query(Article))\
            .join(Author)\
            .join(User)\
            .filter(User.username == author_name)\
            .all()
    else:
        articles = Article.query.all()
    return render_template('articles/list.html',
                           articles=articles,
                           tag=tag_name,
                           author_name=author_name
                           )


@articles_app.route('/<int:article_id>/', endpoint='details')
def article_details(article_id: int):
    article = Article.query.filter_by(id=article_id).options(
        joinedload(Article.tags)
    ).one_or_none()

    if article is None:
        raise NotFound
    return render_template('articles/details.html', article=article)


@articles_app.route('/create/', methods=['GET', 'POST'], endpoint='create')
@login_required
def create_article():
    error = None
    form = CreateArticleForm(request.form)
    form.tags.choices = [
        (tag.id, tag.name)
        for tag in Tag.query.order_by('name')
    ]
    if request.method == 'POST' and form.validate_on_submit():
        article = Article(title=form.title.data.strip(), body=form.body.data)

        if current_user.author:
            article.author_id = current_user.author.id
        else:
            author = Author(user_id=current_user.id)
            db.session.add(author)
            db.session.flush()
            article.author_id = author.id

        if form.tags.data:
            selected_tags = Tag.query.filter(Tag.id.in_(form.tags.data))
            for tag in selected_tags:
                article.tags.append(tag)

        db.session.add(article)
        try:
            db.session.commit()
        except IntegrityError:
            current_app.logger.exception('Could not create a new article!')
            error = 'Could not create article!'
        else:
            return redirect(url_for(
                'articles_app.details',
                article_id=article.id),
            )
    return render_template('articles/create.html', form=form, error=error)


@articles_app.route('/<int:article_id>/edit',
                    methods=['GET', 'POST'],
                    endpoint='edit')
@login_required
def edit_article(article_id: int):
    error = None

    article = Article.query.filter_by(id=article_id).one_or_none()
    if article is None:
        raise NotFound
    if article.author_id != current_user.author.id \
            and not current_user.is_staff:
        return abort(403)
    article_tags = [tag.name for tag in article.tags]

    form = EditArticleForm()
    form.title.data = article.title
    form.body.data = article.body
    form_tags = [(tag.id, tag.name) for tag in
                 Tag.query.order_by('name')]

    if request.method == 'POST' and form.validate_on_submit():
        article.title = form.title.data.strip()
        article.body = form.body.data
        form_selected_tags = request.form.getlist('tags')

        article.tags.clear()
        for tag in Tag.query.filter(Tag.id.in_(form_selected_tags)).all():
            article.tags.append(tag)

        try:
            db.session.commit()
        except IntegrityError:
            current_app.logger.exception('Could not edit article!')
            error = 'Could not edit article!'
        else:
            return redirect(url_for(
                'articles_app.details',
                article_id=article.id),
            )
    return render_template(
        'articles/edit.html',
        form=form,
        error=error,
        article=article,
        form_tags=form_tags,
        article_tags=article_tags,
    )
