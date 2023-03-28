from flask import redirect, url_for
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from flask_login import current_user

from blog import models
from blog.models.database import db


class MyAdminIndexView(AdminIndexView):

    @expose()
    def index(self):
        if not (current_user.is_authenticated and current_user.is_staff):
            return redirect(url_for('auth_app.login'))
        return super(MyAdminIndexView, self).index()


class CustomView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_staff

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth_app.login'))


class TagAdminView(CustomView):
    column_searchable_list = ('name',)
    column_filters = ('name',)
    can_export = True
    export_types = ['csv', 'xlsx']
    create_modal = True
    edit_modal = True


class UserAdminView(CustomView):
    column_exclude_list = ('_password',)
    column_searchable_list = (
        'first_name',
        'last_name',
        'username',
        'is_staff',
        'email',
    )
    column_filters = (
        'first_name',
        'last_name',
        'username',
        'is_staff',
        'email',
    )
    column_editable_list = ('first_name', 'last_name', 'is_staff')
    can_create = True
    can_edit = True
    can_delete = False


class AuthorAdminView(CustomView):
    column_list = ('user.username',)
    column_labels = {'user.username': 'Username'}


class ArticleAdminView(CustomView):
    column_list = ('article.title',)
    column_labels = {'article.title': 'Title'}


admin = Admin(
    name='Blog Admin',
    template_mode='bootstrap4',
    index_view=MyAdminIndexView(),
)

admin.add_view(ArticleAdminView(models.Article, db.session, category='Models'))
admin.add_view(TagAdminView(models.Tag, db.session, category='Models'))
admin.add_view(AuthorAdminView(models.Author, db.session, category='Models'))
admin.add_view(UserAdminView(models.User, db.session, category='Models'))

admin.add_link(MenuLink(name='Back to site', url='/'))
admin.add_link(MenuLink(name='Logout', url='/logout'))
