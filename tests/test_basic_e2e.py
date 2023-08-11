"""Module contains basic end-to-end (e2e) tests."""
import re

import pytest
from playwright.sync_api import Locator, Page, expect

BASE_URL = "http://127.0.0.1:5000"

SELECTED_PATTERN = re.compile("selected")


@pytest.fixture(autouse=True)
def _start_page(page: Page) -> None:
    """Go to the start page."""
    page.goto(BASE_URL)


def test_home_redirect(page: Page) -> None:
    """Going to `/` should redirect to `/login`."""
    expect(page).to_have_url(f"{BASE_URL}/login")


BtnContentPair = tuple[Locator, Locator]


def _test_first_selected_second_not(
    selected: BtnContentPair,
    not_selected: BtnContentPair,
) -> None:
    for sel in selected:
        expect(sel).to_have_class(SELECTED_PATTERN)
    for not_sel in not_selected:
        expect(not_sel).not_to_have_class(SELECTED_PATTERN)


def test_page_nav(page: Page) -> None:
    """Test clicking some content buttons and check content visbility toggle."""
    btns = page.locator("#contentButtons")
    login_button = btns.locator("#loginButton")
    members_button = btns.locator("#membersButton")

    login_button_content_pair = login_button, page.locator("#login")

    members_button_content_pair = members_button, page.locator("#members")

    pairs = login_button_content_pair, members_button_content_pair

    # start off at login
    _test_first_selected_second_not(*pairs)

    # [::1] reverses an iterable.

    # flip it!
    members_button.click()
    pairs = pairs[::-1]
    _test_first_selected_second_not(*pairs)

    # last flip
    login_button.click()
    pairs = pairs[::-1]
    _test_first_selected_second_not(*pairs)
