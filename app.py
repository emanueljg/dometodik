"""A module containing flask app init and routes."""

from flask import Flask, redirect, request
from flask.scaffold import T_route
from flask_login import login_user, logout_user, login_required, current_user
from typing import Any
from collections.abc import Callable
from datetime import date

from .auth import init_flask_login
from .helpers import base_render
from .content import Content
from .user import User
from .calendar import Calendar, Todo


app = Flask(__name__)
with open("flask_secret", "r") as f:
    app.secret_key = f.read()
init_flask_login(app)

Route = Callable[[T_route], T_route]


d1 = date(year=2023, month=1, day=1)
t1 = Todo(d1, "todo1")
t2 = Todo(d1, "todo2")
CAL = Calendar(d1)
CAL.add_todo(t1)
CAL.add_todo(t2)


@app.route("/")
def base() -> Any:
    return redirect("/home")


@app.route("/login", methods=(["POST"]))
def login() -> Any:
    """Login a user."""
    if current_user.is_authenticated:
        return redirect("/")

    email = request.form.get("email")
    password = request.form.get("password")
    found_user = User.with_login(email, password)
    if found_user:
        login_user(User.USERS[found_user.id])
        return redirect("/")
    else:
        return base_render(route="login", failed_login=True)


@app.route("/logout", methods=(["GET"]))
@login_required  # type: ignore
def logout() -> Any:
    logout_user()
    return redirect("/login")


@app.route("/change-cal-unit", methods=(["POST"]))
@login_required  # type: ignore
def change_cal_unit() -> Any:
    try:
        month = int(request.args.get("month") or CAL.current_date.month)
        year = int(request.args.get("year") or CAL.current_date.year)
        CAL.current_date = CAL.current_date.replace(month=month, year=year)
    except (ValueError, TypeError):
        pass  # just redirect anyway later
    finally:
        return redirect("/calendar")


@app.route(f'/<any({", ".join(Content.HAS_TEXT())}):content>')
def content_route(content: str) -> Any:
    return base_render(route=content, calendar=CAL)
