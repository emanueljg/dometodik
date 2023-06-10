from collections.abc import Callable
from typing import Any, TypeVar

from flask import Flask

F = TypeVar("F", bound=Callable[..., Any])

class LoginManager:
    def init_app(self, app: Flask, add_context_processor: bool = ...) -> None: ...
    def user_loader(self, callback: F) -> F: ...
