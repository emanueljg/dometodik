"""Module containing the User class etc"""

from flask_login import UserMixin
from typing import Union, Optional
from .helpers import elems_with_attrs
__all__ = ["UserMixin"]
Users = dict[str, "User"]
class User(UserMixin):  # type: ignore
    USERS: Users = {}

    def __init__(self, id: Union[int, str], email: str, password: str):
        self._id = id
        self.email = email
        self.password = password
        self.USERS[str(id)] = self

    @property
    def id(self) -> str:
        return str(self._id)

    @classmethod
    def with_login(cls, email: Optional[str], password: Optional[str]) -> "User":
        return next(
            elems_with_attrs(cls.USERS, email=email, password=password), (None, None)
        )[
            1
        ]  # type: ignore


ADMIN = User(1, "foo", "bar")
