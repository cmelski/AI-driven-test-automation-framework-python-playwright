
from page_objects.shop import ShopPage
from page_objects.login import LoginPage
import tests.helpers.test_assertions as test_assertions
from tests.conftest import logger_utility


def execute_step(page, step):
    action = step["action"]
    params = step.get("parameters", {})

    if action == "login":
        # page.goto("https://www.saucedemo.com")
        # conftest.py already has logic to go to the base url
        page.fill("#user-name", params["user"])
        page.fill("#password", params["password"])
        page.click("#login-button")

    elif action == "add_to_cart":
        shop = ShopPage(page)
        shop.add_product_to_cart(params["product_name"])

    elif action == "open_cart":
        shop = ShopPage(page)
        shop.open_cart()

    elif action == "view_product":
        shop = ShopPage(page)
        shop.get_product_info(params["product_name"])
        product = params["product_name"]
        logger_utility().info(f'View Product spec triggered. {product} is being viewed')

    elif action == "waitForSelector":
        page.wait_for_selector(params["selector"])
        logger_utility().info('Waiting for product details to load')

    else:
        raise ValueError(f"Unknown action: {action}")


def execute_invalid_login_tests(page, spec):
    login_page = LoginPage(page)

    for data in spec["test_data"]:
        # Navigate fresh for each test
        page.goto("https://www.saucedemo.com")

        # Fill in credentials
        login_page.invalid_login(data["user"], data["password"])
        logger_utility().info(f'Attempting to login using Username: {data["user"]} and Password: {data["password"]}')

        # Assert error message
        test_assertions.assert_invalid_login_error(login_page, data["expected_error"])
        logger_utility().info(f'Username and/or Password incorrect')


def execute_assertion(page, assertion):
    if "cart_contains" in assertion:
        test_assertions.assert_cart_contains(
            page,
            assertion["cart_contains"]["product_name"]
        )
    elif "shop_page_loaded" in assertion:
        test_assertions.assert_shop_page_loaded_after_login(
            page,
            assertion["shop_page_loaded"]["page_title"]
        )


def execute_product_assertions(page, assertion):
    if "product_details" in assertion:
        for item in assertion["product_details"]:
            test_assertions.execute_product_detail_assertion(page, item)
    else:
        raise ValueError(f"Unknown assertion type: {assertion}")
