from pytest import fixture
import re
from playwright.sync_api import Page, expect, Locator

BASE_URL = "http://127.0.0.1:5000"

SELECTED_PATTERN = re.compile("selected")


@fixture(scope="function", autouse=True)
def start_page(page: Page) -> None:
    page.goto(BASE_URL)


def test_home_redirect(page: Page) -> None:
    expect(page).to_have_url(f"{BASE_URL}/home")


BtnContentPair = tuple[Locator, Locator]


def _test_first_selected_second_not(
    selected: BtnContentPair, not_selected: BtnContentPair
) -> None:
    for sel in selected:
        expect(sel).to_have_class(SELECTED_PATTERN)
    for not_sel in not_selected:
        expect(not_sel).not_to_have_class(SELECTED_PATTERN)


def test_page_nav(page: Page) -> None:
    btns = page.locator("#contentButtons")
    home_button = btns.locator("#homeButton")
    members_button = btns.locator("#membersButton")

    home_button_content_pair = home_button, page.locator("#home")

    members_button_content_pair = members_button, page.locator("#members")

    pairs = home_button_content_pair, members_button_content_pair

    # start off at home
    _test_first_selected_second_not(*pairs)

    # [::1] reverses an iterable.
    # (1, 2, 3)[::-1] = (3, 2, 1)

    # flip it!
    members_button.click()
    pairs = pairs[::-1]
    _test_first_selected_second_not(*pairs)

    # last flip
    home_button.click()
    pairs = pairs[::-1]
    _test_first_selected_second_not(*pairs)
