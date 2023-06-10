from collections.abc import Callable
from datetime import timedelta
from typing import Any, TypeVar

from _typeshed import Incomplete

from .mixins import UserMixin

current_user: Incomplete

F = TypeVar("F", bound=Callable[..., Any])

def login_user(
    user: UserMixin,
    remember: bool = ...,
    duration: timedelta | None = ...,
    force: bool = ...,
    fresh: bool = ...,
) -> bool: ...
def logout_user() -> bool: ...
def confirm_login() -> None: ...
def login_required(func: F) -> F: ...
