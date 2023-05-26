"""A module containing flask_login stuff """

__all__ = [
    'init_flask_login',
    'load_user'
]

from flask_login import LoginManager

from .user import User


_login_manager = LoginManager()

def init_flask_login(app):
    _login_manager.init_app(app)

@_login_manager.user_loader
def load_user(user_id):
    return User.USERS[user_id]

