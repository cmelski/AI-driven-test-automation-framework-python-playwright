from page_objects.shop import ShopPage
import re
from playwright.sync_api import expect
from tests.conftest import logger_utility


def validate_shop_page(page_instance, logger_utility, get_products):
    try:
        assert len(get_products) > 0
        logger_utility.info('Products data file contains at least 1 product')
    except AssertionError:
        logger_utility.error('Products data file empty. Test Failed')
        raise

    shop_page = ShopPage(page_instance)
    logger_utility.info(f'Shop URL: {shop_page.url}')
    logger_utility.info(f'Successfully bypassed Login screen for this test')
    # more flexible (reg ex) to make sure inventory.html is in the url
    url_string_to_match = 'inventory'
    try:
        regex_pattern = re.compile(rf"/{re.escape(url_string_to_match)}\.html$")
        expect(shop_page.page).to_have_url(regex_pattern)
        logger_utility.info(f'URL contains "{url_string_to_match}"')
    except AssertionError:
        logger_utility.error(f'URL does not contain "{url_string_to_match}". Test Failed')
        raise

    # assert there are items to select and fail the test and log the error to test_failures.log
    try:
        expect(shop_page.inventory_items).not_to_have_count(0)
    except AssertionError:
        logger_utility.error("Inventory count is 0. Test Failed", exc_info=True)
        raise

    inventory_count = shop_page.inventory_items.count()
    logger_utility.info(f'Shop Page Inventory Count: {inventory_count}')

    return shop_page


def assert_cart_contains(page, product_name):
    cart_items = page.locator(".cart_item").filter(has_text=product_name)
    expect(cart_items).to_have_count(1)
    logger_utility().info(f'Cart correctly has 1 item: {product_name}')


def assert_shop_page_loaded_after_login(page, page_title):
    expect(page.locator('.title')).to_have_text(page_title)


def assert_invalid_login_error(page, error):
    expect(page.login_error).to_contain_text(error)


def execute_product_detail_assertion(page, item):
    selector = item["selector"]
    logger_utility().info(f'Selector: {selector}')
    locator = page.locator(selector)
    logger_utility().info(f'Locator: {locator}')

    if "toHaveText" in item:
        expect(locator).to_have_text(item["toHaveText"])

    if "toBeVisible" in item and item["toBeVisible"] is True:
        expect(locator).to_be_visible()



