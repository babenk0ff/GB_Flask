from flask_login import UserMixin
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, Boolean

from blog.models.database import db


class User(db.Model, UserMixin):

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    first_name = Column(String(80), nullable=True)
    last_name = Column(String(80), nullable=True)
    email = Column(db.String(255), unique=True, nullable=False)
    _password = Column(String, nullable=False)
    is_staff = Column(Boolean, nullable=False, default=False)

    author = relationship('Author', uselist=False, back_populates='user')

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = generate_password_hash(value)

    def validate_password(self, password) -> bool:
        return check_password_hash(self._password, password)
