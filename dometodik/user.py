"""Module containing the User class etc."""


import itertools
import json
from pathlib import Path
from typing import Optional

from flask_login import UserMixin

from .helpers import elems_with_attrs

__all__ = ["Users", "User"]


class User(UserMixin):
    """A class that defines a user."""

    def __init__(  # noqa: PLR0913
        self: "User",
        id_: int | str,
        firstname: str,
        lastname: str,
        role: str,
        email: str,
        password: str,
    ) -> None:
        """Init the user and add them to the list of all users."""
        self._id = id_
        self.firstname = firstname
        self.lastname = lastname
        self.role = role
        self.email = email
        self.password = password

    @property
    def id(self: "User") -> str:  # noqa: A003  # pylint: disable=invalid-name
        """Return the user ID."""
        return str(self._id)


class Users(dict[int, User]):
    """A mapping of `User` IDs and the users they correspond to."""

    counter = itertools.count()

    def __init__(self: "Users", json_path: Path = Path("./members.json")) -> None:
        """Init a Users dict."""
        self.json_path = json_path
        super().__init__()

    def load(self: "Users") -> "Users":
        """Load all users from a json doc."""
        with Path.open(self.json_path) as f:
            json_elems = json.loads(f.read())
            for json_elem in json_elems:
                id_ = next(Users.counter)
                user = User(
                    id_=id_,
                    firstname=json_elem["firstname"],
                    lastname=json_elem["lastname"],
                    role=json_elem["role"],
                    email=json_elem["email"],
                    password=json_elem["password"],
                )
                self[id_] = user
        return self

    def with_login(
        self: "Users",
        email: str | None,
        password: str | None,
    ) -> Optional["User"]:
        """Return the user with the required credentials, or `None`."""
        return next(
            elems_with_attrs(self, email=email, password=password),
            (None, None),
        )[1]
