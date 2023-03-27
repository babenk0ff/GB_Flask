from flask import request
from combojsonapi.permission import PermissionMixin, PermissionUser, \
    PermissionForPatch
from flask_login import current_user

from blog.models import Article


class ArticlePatchPermission(PermissionMixin):
    AVAILABLE_FIELDS_FOR_PATCH = ['title', 'body']

    def patch_permission(
            self,
            *args,
            user_permission: PermissionUser = None,
            **kwargs,
    ) -> PermissionForPatch:

        if request.endpoint == 'edit':
            article = Article.query.filter_by(
                id=request.view_args['article_id']
            ).one_or_none()
            if article.author_id == current_user.author.id:
                self.permission_for_patch.allow_columns = (
                    self.AVAILABLE_FIELDS_FOR_PATCH, 10
                )
        return self.permission_for_patch

    def patch_data(
            self,
            *args,
            data=None,
            obj=None,
            user_permission: PermissionUser = None,
            **kwargs,
    ) -> dict:

        permission_for_patch = user_permission.permission_for_patch_permission(
            model=Article,
        )
        return {
            key: val
            for key, val in data.items()
            if key in permission_for_patch
        }
