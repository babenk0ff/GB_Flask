import click
from werkzeug.security import generate_password_hash
from blog.models.database import db


@click.command('init-db')
def init_db():
    db.create_all()
    print('Database created')


@click.command('create-users')
def create_users():
    from blog.models import User
    admin = User(
        username='admin',
        email='admin@mail.local',
        password=generate_password_hash('qwerty'),
        is_staff=True
    )
    james = User(
        username='james',
        email='james@mail.local',
        password=generate_password_hash('james')
    )

    db.session.add(admin)
    db.session.add(james)
    db.session.commit()

    print('Created users:', admin, james)
