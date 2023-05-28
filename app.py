"""A module containing flask app init and routes."""

from flask import Flask, redirect, url_for, render_template, request
from flask.scaffold import T_route
from flask_login import login_user, logout_user, login_required, current_user
from dataclasses import dataclass
from typing import Collection, ClassVar, Any
from collections.abc import Callable

from .auth import init_flask_login, load_user
from .helpers import elems_with_attrs, base_render
from .content import Content
from .user import User


app = Flask(__name__)
app.secret_key = '9a5696420b61932bf0690347fd0a7653e62091ff8f359dc1bbfbec461caf22d3'
init_flask_login(app)

Route = Callable[[T_route], T_route]

@app.route('/login', methods=(['POST']))
def login() -> Any:
    """Login a user."""
    if current_user.is_authenticated:
        return redirect('/')
    
    email = request.form.get('email')
    password = request.form.get('password')
    found_user = User.with_login(email, password)
    if found_user:
        login_user(User.USERS[found_user.id])
        return redirect('/')
    else:
        return base_render(route='login', failed_login=True) 
        
@app.route('/logout', methods=(['GET']))
@login_required  # type: ignore
def logout() -> Any:
    logout_user()
    return redirect('/login')


@app.route(f'/<any({", ".join(Content.HAS_TEXT())}):content>')
def content_route(content: str) -> Any:
    return base_render(route=content)

@app.route('/')
def base() -> Any:
    return redirect('/home')

