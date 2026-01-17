from page_objects.shop import ShopPage
import re
from playwright.sync_api import expect


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
