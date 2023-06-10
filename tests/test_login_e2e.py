"""A module containing authentication end-to-end (e2e) tests."""
import pytest
from playwright.sync_api import Locator, Page, _generated, expect

BASE_URL = "http://127.0.0.1:5000"


class Status:
    """Just some status codes."""

    # pylint: disable=too-few-public-methods

    SUCCESS = 200
    UNAUTHORIZED = 401


def goto(page: Page, route: str) -> _generated.Response | None:
    """Goto the page `page` with the route `route`."""
    return page.goto(f"{BASE_URL}/{route}")


@pytest.fixture(autouse=True)
def _start_page(page: Page) -> None:
    """Go to the start page."""
    page.goto(BASE_URL)


def test_forbiddens(page: Page) -> None:
    """Test that unauthorized can't access locked routes."""
    resp = goto(page, "logout")
    assert resp is not None
    assert resp.status == Status.UNAUTHORIZED


def _locate_login_fail(login: Locator) -> Locator:
    return login.locator("#failed-login")


def _do_login(page: Page, email: str, password: str, *, do_goto: bool = False) -> None:
    if do_goto:
        goto(page, "login")
    login = page.locator("#login")

    login.locator("#email").fill(email)
    login.locator("#password").fill(password)
    login.get_by_role("button", name="Submit").click()


def test_bad_login(page: Page) -> None:
    """Test login with bad credentials."""
    goto(page, "login")
    login = page.locator("#login")

    # no login fail since we haven't logged in yet
    expect(_locate_login_fail(login)).to_be_hidden()

    _do_login(page, "bomb", "bomb")

    # expect login fail
    expect(_locate_login_fail(login)).to_be_visible()


def test_good_login(page: Page) -> None:
    """Test login with good credentials."""
    # login
    _do_login(page, "foo", "bar", do_goto=True)

    # should be back to home
    expect(page).to_have_url(f"{BASE_URL}/home")

    # logout
    resp = goto(page, "logout")
    assert resp is not None
    assert resp.status == Status.SUCCESS

    # should be back to login
    expect(page).to_have_url(f"{BASE_URL}/login")

    # now we can't logout again
    resp = goto(page, "logout")
    assert resp is not None
    assert resp.status == Status.UNAUTHORIZED
