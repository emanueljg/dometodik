"""A module containing flask_login stuff """

__all__ = [
    'init_flask_login',
    'load_user'
]

from flask.app import Flask
from flask_login import LoginManager

from .user import User


_login_manager = LoginManager()

def init_flask_login(app: Flask) -> None:
    _login_manager.init_app(app)

@_login_manager.user_loader  # type: ignore
def load_user(user_id) -> User:
    return User.USERS[user_id]

