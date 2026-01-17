import json
import re

import pytest
from playwright.sync_api import expect
from tests.helpers.common_test_setup_assertions import validate_shop_page


@pytest.fixture()
def get_products():
    with open('data/products.json') as f:  # path is relative to project root
        products = json.load(f)['products']
        return products


@pytest.mark.build_shopping_cart
def test_build_shopping_cart(page_instance, logger_utility, get_products):

    shop_page = validate_shop_page(page_instance,logger_utility,get_products)

    # assert that all items from get_products fixture exist in the shop page
    # if a product exists, add it to cart

    cart = dict()

    for product in get_products:
        product_name = product['product_name']
        shop_page_product = shop_page.inventory_product_names.filter(
            has_text=re.compile(rf"\b{re.escape(product_name)}\b")
        )
        try:
            logger_utility.info(f'shop page product count: {shop_page_product.count()}')
            expect(shop_page_product).to_have_count(1)
            logger_utility.info(f"{product['product_name']} found")
            cart[product_name] = shop_page.add_product_to_cart(product_name)
        except AssertionError:
            logger_utility.error(
                f"Shop page does not have this product: {product['product_name']}"
            )
            raise

        logger_utility.info(f'Shopping cart details: {cart}')

        # next view the shopping cart and verify number of items and the cart details




