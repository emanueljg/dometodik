from pytest import fixture
from playwright.sync_api import Page, expect

BASE_URL = 'http://127.0.0.1:5000'

@fixture(scope="function", autouse=True)
def start_page(page: Page) -> None:
    page.goto(BASE_URL)

def test_home_redirect(page: Page) -> None:
    expect(page).to_have_url(f'{BASE_URL}/home')
