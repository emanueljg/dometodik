"""A module containing flask app init and routes."""

from collections.abc import Callable
from datetime import date

from flask import Flask, redirect, request
from flask.scaffold import T_route
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.wrappers.response import Response

from .auth import init_flask_login
from .calendar import Calendar, Todo
from .content import Content
from .helpers import base_render
from .user import User

app = Flask(__name__)
app.secret_key = "not very secret..."  # noqa: S105

init_flask_login(app)

Route = Callable[[T_route], T_route]


d1 = date(year=2023, month=1, day=1)
t1 = Todo(d1, "todo1")
t2 = Todo(d1, "todo2")
CAL = Calendar(d1)
CAL.add_todo(t1)
CAL.add_todo(t2)


@app.route("/")
def base() -> Response:
    """Redirect root route to /home."""
    return redirect("/home")


@app.route("/login", methods=(["POST"]))
def login() -> Response | str:
    """Login a user."""
    if current_user.is_authenticated:
        return redirect("/")

    email = request.form.get("email")
    password = request.form.get("password")
    found_user = User.with_login(email, password)
    if found_user:
        login_user(User.USERS[found_user.id])
        return redirect("/")
    return base_render(route="login", failed_login=True)


@app.route("/logout", methods=(["GET"]))
@login_required
def logout() -> Response:
    """Logout the user and redirect to login page."""
    logout_user()
    return redirect("/login")


@app.route("/change-cal-unit", methods=(["POST"]))
@login_required
def change_cal_unit() -> Response:
    """Change the calendars month or year."""
    try:
        month = int(request.args.get("month") or CAL.current_date.month)
        year = int(request.args.get("year") or CAL.current_date.year)
        CAL.current_date = CAL.current_date.replace(month=month, year=year)
    except (ValueError, TypeError):
        pass  # just redirect anyway later
    return redirect("/calendar")


@app.route(f'/<any({", ".join(Content.with_text())}):content>')
def content_route(content: str) -> str:
    """Return a base html with the routed conted active."""
    return base_render(route=content, calendar=CAL)
