from page_objects.cart import CartPage
from page_objects.login import LoginPage
from page_objects.product import ProductPage
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
    cart_page = CartPage(page)
    if "product_names" in item:
        product_count = len(item["product_names"])
        cart_product_count = 0
        for product_text in item["product_names"]:
            cart_items = cart_page.cart_items.filter(has_text=product_text)
            if cart_items:
                logger_utility().info(f'{product_text} correctly found in cart')
                cart_product_count += 1

        assert product_count == cart_product_count, 'Cart details incorrect'
        logger_utility().info(f'Cart correctly has {product_count} items')

    else:
        raise ValueError(f"Unknown assertion tag: 'toHaveText'")


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
    product_page = ProductPage(page)
    element = item["name"]

    if element == 'product_page_loaded':
        page.wait_for_selector(product_page.product_details_panel_selector)
        logger_utility().info('Product page is loaded')

    if element == 'product_name':
        toHaveText = item["toHaveText"]
        expect(product_page.product_name).to_have_text(toHaveText)
        logger_utility().info(f'{toHaveText} is displayed')

    if element == 'product_description':
        toBeVisible = item["toBeVisible"]
        expect(product_page.product_description).to_be_visible()
        logger_utility().info(f'{element} visibility is {toBeVisible}')

    if element == 'product_price':
        toBeVisible = item["toBeVisible"]
        expect(product_page.product_price).to_be_visible()
        logger_utility().info(f'{element} visibility is {toBeVisible}')

    if element == 'add_to_cart_button':
        toBeVisible = item["toBeVisible"]
        expect(product_page.add_to_cart_button).to_be_visible()
        logger_utility().info(f'{element} visibility is {toBeVisible}')

    if element == 'back_to_shop_button':
        toBeVisible = item["toBeVisible"]
        expect(product_page.back_to_shop_button).to_be_visible()
        logger_utility().info(f'{element} visibility is {toBeVisible}')


def execute_cart_assertions(page, item):
    cart_page = CartPage(page)
    name = item["name"]
    logger_utility().info(f'Assertion name: {name}')

    if name == "cart_item":
        product_name = item["toHaveText"]
        cart_items = cart_page.cart_items.filter(has_text=product_name)
        expect(cart_items).to_have_count(1)
        logger_utility().info(f'Cart correctly has 1 item: {product_name}')

    if name == "cart_badge":
        shopping_cart_size = item["toHaveCount"]
        logger_utility().info(f'Shopping cart items: {shopping_cart_size}')
        expect(cart_page.cart_icon).to_have_count(shopping_cart_size)

        if shopping_cart_size > 0:
            expect(cart_page.cart_icon).to_have_text(str(shopping_cart_size))
            logger_utility().info(f'Cart badge correctly shows: {shopping_cart_size}')
        else:
            logger_utility().info(f'Product removed from shopping cart')
