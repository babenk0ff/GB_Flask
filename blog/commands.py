import os

import click
import sqlalchemy.exc

from blog.models.database import db


@click.command('create-admin')
def create_admin():
    from blog.models import User
    admin = User(
        username='admin',
        email=os.getenv('ADMIN_EMAIL') or 'admin@admin.local',
        password=os.getenv('ADMIN_PASSWORD') or 'admin',
        is_staff=True,
    )

    db.session.add(admin)
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        print(e)
        db.session.close()
    else:
        print('Created admin')


@click.command('create-tags')
def create_tags():
    from blog.models import Tag
    for name in [
        'flask',
        'django',
        'python',
        'sqlalchemy',
        'news',
    ]:
        tag = Tag(name=name)
        db.session.add(tag)
    db.session.commit()
    print('created tags')
