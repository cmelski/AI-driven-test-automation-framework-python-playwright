import os
import logging
import pytest

# load test.env file variables
from dotenv import load_dotenv

from playwright.sync_api import sync_playwright, TimeoutError


# define test run parameters
# in terminal you can run for e.g. 'pytest test_web_framework_api.py --browser_name firefox'
def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome", help="browser selection"
    )

    parser.addoption(
        "--url_start", action="store", default="test", help="starting url"
    )

    parser.addoption(
        "--env", action="store", default="test", help="Environment to run tests against")


@pytest.fixture(scope="session")
def env(request):
    env_name = request.config.getoption("--env")
    # Load the corresponding .env file
    load_dotenv(f"{env_name}.env")
    return env_name


@pytest.fixture(scope="session")
def url_start(env):  # env fixture ensures .env is loaded first
    return os.environ.get("BASE_URL")


@pytest.fixture(scope="session")
def valid_login_credentials(env):  # env fixture ensures .env is loaded first
    valid_username = os.environ.get("VALID_USERNAME")
    valid_password = os.environ.get("VALID_PASSWORD")
    valid_credentials = {'user_name': valid_username,
                         'password': valid_password
                         }
    return valid_credentials

@pytest.fixture
def invalid_login_credentials(request, valid_login_credentials):
    if request.param == "empty":
        return "", ""

    if request.param == "bad_password":
        return valid_login_credentials["user_name"], "bad_password"

    if request.param == "bad_username":
        return "bad_username", valid_login_credentials["password"]

    raise ValueError(f"Unknown param: {request.param}")


@pytest.fixture(scope="session")
def logger_utility():
    # set up logging
    logger = logging.getLogger(__name__)
    return logger


# main tests fixture that yields page object and then closes context and browser after yield as part of teardown
@pytest.fixture(scope='function')
def page_instance(request, url_start, env):
    browser_name = request.config.getoption('browser_name')
    url_start = url_start

    with sync_playwright() as p:
        if browser_name == 'chrome':
            browser = p.chromium.launch(headless=False, timeout=120000)
        elif browser_name == 'firefox':
            browser = p.firefox.launch(headless=False)

        context = browser.new_context()

        page = context.new_page()
        page.goto(url_start)

        try:

            yield page
        finally:
            context.close()
            browser.close()
