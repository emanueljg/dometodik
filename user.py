"""Module containing the User class etc"""

from flask_login import UserMixin

from .helpers import elems_with_attrs

__all__ = ['UserMixin']


class User(UserMixin):
    USERS = {}
    
    def __init__(self, id, email, password): 
        self._id = id
        self.email = email
        self.password = password
        self.USERS[str(id)] = self

    @property
    def id(self):
        return str(self._id)

    @classmethod
    def with_login(cls, email, password):
        return next(elems_with_attrs(
            cls.USERS, 
            email=email,
            password=password), (None, None))[1]


ADMIN = User(1, 'foo', 'bar')
