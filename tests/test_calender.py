"""Module contains basic end-to-end (e2e) tests."""
from datetime import date
from typing import NamedTuple

import pytest
from playwright.sync_api import Page, expect

from .test_login_e2e import _do_login, goto

BASE_URL = "http://127.0.0.1:5000"


@pytest.fixture(autouse=True)
def _calendar_page(page: Page) -> None:
    """Go to the calendar."""
    _do_login(page, "foo", "bar", do_goto=True)
    goto(page, "calendar-setup")


def _add_todo(
    page: Page,
    day: str | None = None,
    text: str | None = None,
) -> date:
    adder = page.locator("#todo-adder")
    _day = adder.locator("input[name=date]")

    if day:
        _day.fill(day)  # noqa: E701
    adder.get_by_role("textbox", name="text").fill(text or "")
    adder.get_by_role("button", name="submit").click()

    return date.fromisoformat(_day.input_value())


def _get_current_date(page: Page) -> date:
    return date.fromisoformat(
        page.locator("#todo-adder").locator("input[name=date]").input_value(),
    )


def _isodate(day: date) -> str:
    return day.strftime("%Y-%m-%d")


def test_add_todo(page: Page) -> None:
    """Test adding a todo."""
    todos = page.locator("#todo-list > .todo")
    expect(todos).to_have_count(0)

    current_date = _get_current_date(page)
    next_date = current_date.replace(day=current_date.day + 1)

    class _Example(NamedTuple):
        day: date
        should_preview: str
        text: str | None

    examples = (
        _Example(current_date, "(1) 1", None),
        _Example(next_date, "(1) 2", "foo"),
        _Example(next_date, "(2) 2, 3", "bar"),
    )

    for num, example in enumerate(examples):
        day, should_preview, text = example
        _add_todo(page, day=_isodate(day), text=text)

        # check todo list
        expect(todos).to_have_count(num + 1)
        todo = todos.nth(num)
        expect(todo).to_contain_text(f"({num + 1}) {_isodate(day)} ")
        if text:
            expect(todo).to_contain_text(text)  # noqa: E701

        # check calendar list
        cal_day = page.locator(".calendar-day").nth(day.day - 1)
        expect(cal_day).to_contain_text(should_preview)


def test_change_todo(page: Page) -> None:
    """Test changing a todo."""
    current_date = _get_current_date(page)
    current_date_iso = _isodate(current_date)
    next_date = current_date.replace(day=current_date.day + 1)
    next_date_iso = _isodate(next_date)

    _add_todo(page, day=_isodate(current_date))

    # start normally
    todo = page.locator("#todo-1")
    expect(todo).to_contain_text(f"(1) {current_date_iso}")

    # let's edit
    todo.locator("#todo-toggler-1").click()
    editor = page.locator("#todo-editor-1")
    expect(editor).to_be_visible()
    editor.locator("input[name=date]").fill(next_date_iso)
    editor.locator("textarea[name=text]").fill("foo")
    editor.locator("input[type=submit]").click()

    # should now be chaged
    expect(todo).to_contain_text(f"(1) {next_date_iso}")
    expect(todo).to_contain_text("foo")


def test_delete_todo(page: Page) -> None:
    """Test deleting a todo."""
    _add_todo(page)
    todos = page.locator("#todo-list > .todo")
    expect(todos).to_have_count(1)
    todos.locator("#todo-deleter-1").click()
    expect(todos).to_have_count(0)
