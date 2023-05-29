from pytest import fixture
from typing import Optional
from playwright.sync_api import Page, expect, Locator, _generated


BASE_URL = "http://127.0.0.1:5000"


def goto(page: Page, route: str) -> Optional[_generated.Response]:
    return page.goto(f"{BASE_URL}/{route}")


@fixture(scope="function", autouse=True)
def start_page(page: Page) -> None:
    page.goto(BASE_URL)


def test_forbiddens(page: Page) -> None:
    resp = goto(page, "logout")
    assert resp is not None and resp.status == 401


def _locate_login_fail(login: Locator) -> Locator:
    return login.locator("#failed-login")


def _do_login(page: Page, email: str, password: str, do_goto: bool = False) -> None:
    if do_goto:
        goto(page, "login")
    login = page.locator("#login")

    login.locator("#email").fill(email)
    login.locator("#password").fill(password)
    login.get_by_role("button", name="Submit").click()


def test_bad_login(page: Page) -> None:
    goto(page, "login")
    login = page.locator("#login")

    # no login fail since we haven't logged in yet
    expect(_locate_login_fail(login)).to_be_hidden()

    _do_login(page, "bomb", "bomb")

    # expect login fail
    expect(_locate_login_fail(login)).to_be_visible()


def test_good_login(page: Page) -> None:
    # login
    _do_login(page, "foo", "bar", do_goto=True)

    # should be back to home
    expect(page).to_have_url(f"{BASE_URL}/home")

    # logout
    resp = goto(page, "logout")
    assert resp is not None and resp.status == 200

    # should be back to login
    expect(page).to_have_url(f"{BASE_URL}/login")

    # now we can't logout again
    resp = goto(page, "logout")
    assert resp is not None and resp.status == 401
