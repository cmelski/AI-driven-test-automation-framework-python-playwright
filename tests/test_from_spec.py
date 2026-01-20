import yaml
import pytest
from tools.spec_runner import execute_step, execute_assertion, execute_invalid_login_tests, execute_product_assertions
from tools.utils import substitute_env_vars, replace_placeholders
from tests.conftest import logger_utility


@pytest.mark.feature("BUILD_CART")
def test_build_cart_from_yaml_spec(page_instance_login):
    with open("features/generated/build_cart.yaml") as f:
        spec = yaml.safe_load(f)
    spec = substitute_env_vars(spec)
    spec = replace_placeholders(spec)
    logger_utility().info(f'YAML build_cart feature file loaded: {spec} ')

    for step in spec["steps"]:
        execute_step(page_instance_login, step)

    for assertion in spec["assertions"]:
        execute_assertion(page_instance_login, assertion)


@pytest.mark.feature("AUTH_LOGIN")
def test_valid_login_from_yaml_spec(page_instance_login):
    with open("features/generated/auth_login.yaml") as f:
        spec = yaml.safe_load(f)
    spec = substitute_env_vars(spec)
    logger_utility().info(f'YAML auth_login feature file loaded: {spec} ')

    for step in spec["steps"]:
        execute_step(page_instance_login, step)

    for assertion in spec["assertions"]:
        execute_assertion(page_instance_login, assertion)


@pytest.mark.feature("INVALID_LOGIN")
def test_invalid_logins_from_yaml_spec(page_instance_login):
    with open("features/generated/invalid_login.yaml") as f:
        spec = yaml.safe_load(f)
    spec = substitute_env_vars(spec)
    logger_utility().info(f'YAML auth_login feature file loaded: {spec} ')

    execute_invalid_login_tests(page_instance_login, spec)


@pytest.mark.feature("VIEW_PRODUCT")
def test_view_product_from_yaml_spec(page_instance):
    with open("features/generated/view_product.yaml") as f:
        spec = yaml.safe_load(f)
    spec = substitute_env_vars(spec)
    spec = replace_placeholders(spec)
    logger_utility().info(f'YAML view feature file loaded: {spec} ')

    for step in spec["steps"]:
        execute_step(page_instance, step)

    for assertion in spec["assertions"]:
        execute_product_assertions(page_instance, assertion)
