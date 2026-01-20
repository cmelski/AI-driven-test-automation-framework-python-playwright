import json
import os


def substitute_env_vars(d):
    """Recursively replace ${VAR} in dict with environment variables"""
    if isinstance(d, dict):
        return {k: substitute_env_vars(v) for k, v in d.items()}
    elif isinstance(d, list):
        return [substitute_env_vars(x) for x in d]
    elif isinstance(d, str):
        # replace ${VAR} or $VAR
        for key, value in os.environ.items():
            d = d.replace(f"${{{key}}}", value).replace(f"${key}", value)
        return d
    else:
        return d


with open("data/products.json") as f:
    products_data = json.load(f)["products"]

# Map placeholder keys to JSON values
placeholder_map = {
    "${PRODUCT_1}": products_data[0]["product_name"],
    "${PRODUCT_2}": products_data[1]["product_name"]
}


def replace_placeholders(d):
    """Recursively replace placeholders in dict with values from JSON"""
    if isinstance(d, dict):
        return {k: replace_placeholders(v) for k, v in d.items()}
    elif isinstance(d, list):
        return [replace_placeholders(x) for x in d]
    elif isinstance(d, str):
        for placeholder, value in placeholder_map.items():
            d = d.replace(placeholder, value)
        return d
    else:
        return d
