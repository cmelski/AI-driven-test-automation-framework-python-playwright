import pytest
from playwright.sync_api import expect
from page_objects.shop import ShopPage
import re


@pytest.mark.view_product_info
def test_view_product_info_page(page_instance, logger_utility):
    shop_page = ShopPage(page_instance)
    logger_utility.info(f'Shop URL: {shop_page.url}')
    #The following line can’t work because shop_page.url is a string, not a Playwright object
    # and expect() in Playwright only works with Page, Locator, or APIResponse objects.
    # expect(shop_page.url).to_contain_text('inventory')
    #do this instead (3 ways):
    # simplest(no waiting)
    assert "inventory.html" in shop_page.page.url
    # exact url match (less flexible)
    expect(shop_page.page).to_have_url("https://www.saucedemo.com/inventory.html")
    # more flexible (reg ex)
    expect(shop_page.page).to_have_url(re.compile(r"/inventory\.html$"))
    # assert there are items to select
    try:
        expect(shop_page.inventory_items).not_to_have_count(0)
    except AssertionError:
        logger_utility.error(f'Shop Page inventory count is 0')

    inventory_count = shop_page.inventory_items.count()
    logger_utility.info(f'Shop Page Inventory Count: {inventory_count}')



