from page_objects.login import LoginPage
from page_objects.shop import ShopPage
import re
from playwright.sync_api import expect
from tests.conftest import logger_utility


def validate_shop_page(page_instance, get_products):
    try:
        assert len(get_products) > 0
        logger_utility().info('Products data file contains at least 1 product')
    except AssertionError:
        logger_utility().error('Products data file empty. Test Failed')
        raise

    shop_page = ShopPage(page_instance)
    logger_utility().info(f'Shop URL: {shop_page.url}')
    logger_utility().info(f'Successfully bypassed Login screen for this test')
    # more flexible (reg ex) to make sure inventory.html is in the url
    url_string_to_match = 'inventory'
    try:
        regex_pattern = re.compile(rf"/{re.escape(url_string_to_match)}\.html$")
        expect(shop_page.page).to_have_url(regex_pattern)
        logger_utility().info(f'URL contains "{url_string_to_match}"')
    except AssertionError:
        logger_utility().error(f'URL does not contain "{url_string_to_match}". Test Failed')
        raise

    # assert there are items to select and fail the test and log the error to test_failures.log
    try:
        expect(shop_page.inventory_items).not_to_have_count(0)
    except AssertionError:
        logger_utility().error("Inventory count is 0. Test Failed", exc_info=True)
        raise

    inventory_count = shop_page.inventory_items.count()
    logger_utility().info(f'Shop Page Inventory Count: {inventory_count}')


def assert_cart_contains(page, item):
    selector = item["selector"]
    logger_utility().info(f'Selector: {selector}')
    locator = page.locator(selector)
    logger_utility().info(f'Locator: {locator}')
    if "toHaveText" in item:
        cart_items = locator.filter(has_text=item["toHaveText"])
        expect(cart_items).to_have_count(1)
        logger_utility().info(f'Cart correctly has 1 item: {item["toHaveText"]}')


def assert_login_page_loaded(page, item):
    assertion_name = item["name"]
    logger_utility().info(f'Assertion Name: {assertion_name}')

    if assertion_name == 'url':
        logger_utility().info('reached here')
        url = item["url_text"]
        expect(page).to_have_url(url)
        logger_utility().info(f'Login page loaded: {url}')


def assert_shop_page_loaded_after_login(page, item):
    shop_page = ShopPage(page)
    assertion_name = item["name"]
    logger_utility().info(f'Assertion Name: {assertion_name}')

    if assertion_name == 'page_title':
        toHaveText = item["toHaveText"]
        expect(shop_page.title).to_have_text(toHaveText)
        logger_utility().info(f'Shop page loaded. {toHaveText} title is displayed')

    if assertion_name == 'inventory_count':
        notToHaveCount = item["notToHaveCount"]
        expect(shop_page.inventory_items).not_to_have_count(notToHaveCount)
        logger_utility().info(f'Inventory count is > {notToHaveCount}')


def execute_invalid_login_assertions(page, item):
    login_page = LoginPage(page)
    name = item["name"]
    logger_utility().info(f'Assertion: {name}')

    error_string = item["toHaveText"]
    error_visibility = item["toBeVisible"]

    if error_visibility:
        expect(login_page.login_error).to_be_visible()
        logger_utility().info('Error message element is displayed')

        try:
            expect(login_page.login_error).to_contain_text(error_string)
            logger_utility().info(f'Error message contains: {error_string}. '
                                  f'Full message: {login_page.login_error.inner_text()}')
        except AssertionError:
            logger_utility().error(f'{error_string} not present in error message')


def execute_product_detail_assertion(page, item):
    element = item["name"]
    selector = item["selector"]
    logger_utility().info(f'Selector: {selector}')
    locator = page.locator(selector)
    logger_utility().info(f'Locator: {locator}')

    if "toHaveText" in item:
        expect(locator).to_have_text(item["toHaveText"])
        logger_utility().info(f'{item["toHaveText"]} is displayed')

    if "toBeVisible" in item and item["toBeVisible"] is True:
        expect(locator).to_be_visible()
        logger_utility().info(f'{element} is visible')


def execute_cart_assertions(page, item):
    name = item["name"]
    logger_utility().info(f'Selector: {name}')
    selector = item["selector"]
    logger_utility().info(f'Selector: {selector}')
    locator = page.locator(selector)
    logger_utility().info(f'Locator: {locator}')

    if name == "cart_item":
        product_name = item["toHaveText"]
        cart_items = locator.filter(has_text=product_name)
        expect(cart_items).to_have_count(1)
        logger_utility().info(f'Cart correctly has 1 item: {item["toHaveText"]}')

    if name == "cart_badge":
        shopping_cart_size = item["toHaveCount"]
        logger_utility().info(f'Shopping cart items: {shopping_cart_size}')
        expect(locator).to_have_count(item["toHaveCount"])
