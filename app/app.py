"""A module containing flask app init and routes."""

from collections.abc import Callable
from datetime import date, datetime, timezone

from flask import Flask, redirect, request
from flask.scaffold import T_route
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.wrappers.response import Response

from .auth import init_flask_login
from .calendar import Calendar, Todo
from .content import Content  # pylint: disable=cyclic-import
from .helpers import base_render
from .user import User

app = Flask(__name__)
app.jinja_options = {
    "trim_blocks": True,
    "lstrip_blocks": True,
}
app.secret_key = "not very secret..."  # noqa: S105


init_flask_login(app)

Route = Callable[[T_route], T_route]


d1 = datetime.now(tz=timezone.utc).date()
CAL = Calendar(d1)


@app.route("/")
def base() -> Response:
    """Redirect root route to /home."""
    return redirect("/home")


@app.route("/login", methods=("POST",))
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


@app.route("/logout", methods=("GET",))
@login_required
def logout() -> Response:
    """Logout the user and redirect to login page."""
    logout_user()
    return redirect("/login")


@app.route("/change-cal-unit", methods=("POST",))
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


@app.route("/add-todo", methods=("POST",))
@login_required
def add_todo() -> Response:
    """Add a todo."""
    CAL.add_todo(
        Todo(
            date=date.fromisoformat(request.form["date"]),
            text=request.form["text"],
        ),
    )

    return redirect("/calendar")


@app.route("/remove-todo/<todo>", methods=("POST",))
@login_required
def remove_todo(todo: str) -> Response | tuple[str, int]:
    """Remove a todo."""
    CAL.remove_todo(int(todo))
    return redirect("/calendar")


@app.route("/change-todo/<todo>", methods=("POST",))
@login_required
def change_todo(todo: str) -> Response | tuple[str, int]:
    """Change a todo."""
    for todo_n, found_todo in CAL.todos_of_month:
        if todo_n == int(todo):
            found_todo.date = date.fromisoformat(request.form["date"])
            found_todo.text = request.form["text"] or found_todo.text
            CAL.update_todo(found_todo)
            return redirect("/calendar")

    return "todo not found", 404  # couldn't find todo


@app.route("/calendar-setup")
@login_required
def setup_calendar() -> Response:
    """Clear the calendar. Special route."""
    CAL.todos.clear()
    return redirect("/calendar")


@app.route(f'/<any({", ".join(Content.with_text())}):content>')
def content_route(content: str) -> str:
    """Return a base html with the routed conted active."""
    return base_render(route=content, calendar=CAL)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="3000", debug=True)
