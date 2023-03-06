from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean
from blog.models.database import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = db.Column(db.String(255), default='', server_default='', nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_staff = Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<User #{self.id} {self.username!r}>'
