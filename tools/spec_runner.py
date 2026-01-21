from page_objects.cart import CartPage
from page_objects.shop import ShopPage
from page_objects.login import LoginPage
import tests.helpers.test_assertions as test_assertions
from tests.conftest import logger_utility


def execute_step(page, step):
    action = step["action"]
    params = step.get("parameters", {})

    if action == "login":
        login_page = LoginPage(page)
        login_page.login(user_name=params["user_name"],
                         password=params["password"])

    elif action == "add_to_cart":
        shop = ShopPage(page)
        shop.add_product_to_cart(product_name=params["product_name"],
                                 product_inventory=params["product_inventory_selector"],
                                 inventory_item_name=params["inventory_item_name_selector"],
                                 button_name=params["add_to_cart_button_name"])

    elif action == "open_cart":
        shop = ShopPage(page)
        shop.open_cart(cart_link=params["cart_link_selector"])

    elif action == "remove_product_from_cart":
        cart = CartPage(page)
        cart.remove_product_from_cart(params["product_name"])

    elif action == "view_product":
        shop = ShopPage(page)
        shop.get_product_info(product_to_view=params["product_name"],
                              product_inventory=params["product_inventory_selector"])
        product = params["product_name"]
        logger_utility().info(f'View Product spec triggered. {product} attempted to be viewed')

    elif action == "waitForSelector":
        page.wait_for_selector(params["selector"])
        logger_utility().info('Waiting for product details to load')

    else:
        raise ValueError(f"Unknown action: {action}")


def execute_valid_login_assertions(page, assertion):

    if "login_page_loaded" in assertion:
        for item in assertion["login_page_loaded"]:
            test_assertions.assert_login_page_loaded(page, item)
    elif "shop_page_loaded" in assertion:
        for item in assertion["shop_page_loaded"]:
            test_assertions.assert_shop_page_loaded_after_login(page, item)
    else:
        raise ValueError(f"Unknown assertion type: {assertion}")


def execute_invalid_login_assertions(page, assertion):
    if "login_error" in assertion:
        for item in assertion["login_error"]:
            test_assertions.execute_invalid_login_assertions(page, item)
    else:
        raise ValueError(f"Unknown assertion type: {assertion}")


def execute_build_cart_assertion(page, assertion):
    if "cart_contains" in assertion:
        for item in assertion["cart_contains"]:
            test_assertions.assert_cart_contains(page, item)
    else:
        raise ValueError(f"Unknown assertion type: {assertion}")


def execute_product_assertions(page, assertion):
    if "product_details" in assertion:
        for item in assertion["product_details"]:
            test_assertions.execute_product_detail_assertion(page, item)
    else:
        raise ValueError(f"Unknown assertion type: {assertion}")


def execute_cart_assertions(page, assertion):
    if "cart_details_after_removing_product" in assertion:
        for item in assertion["cart_details_after_removing_product"]:
            test_assertions.execute_cart_assertions(page, item)
    elif "cart_badge_icon" in assertion:
        for item in assertion["cart_badge_icon"]:
            test_assertions.execute_cart_assertions(page, item)

    elif "cart_page" in assertion:
        for item in assertion["cart_page"]:
            test_assertions.execute_cart_assertions(page, item)
    else:
        raise ValueError(f"Unknown assertion type: {assertion}")
