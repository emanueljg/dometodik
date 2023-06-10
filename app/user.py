"""Module containing the User class etc."""


from typing import Optional

from flask_login import UserMixin

from .helpers import elems_with_attrs

__all__ = ["UserMixin"]
Users = dict[str, "User"]


class User(UserMixin):
    """A class that defines a user."""

    USERS: Users = {}

    def __init__(self: "User", id_: int | str, email: str, password: str) -> None:
        """Init the user and add them to the list of all users."""
        self._id = id_
        self.email = email
        self.password = password
        self.USERS[str(id_)] = self

    @property
    def id(self: "User") -> str:  # noqa: A003  # pylint: disable=invalid-name
        """Return the user ID."""
        return str(self._id)

    @classmethod
    def with_login(
        cls: type["User"],
        email: str | None,
        password: str | None,
    ) -> Optional["User"]:
        """Return the user with the required credentials, or `None`."""
        return next(
            elems_with_attrs(cls.USERS, email=email, password=password),
            (None, None),
        )[1]


ADMIN = User(1, "foo", "bar")
