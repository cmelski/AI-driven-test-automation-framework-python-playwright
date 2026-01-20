import os

from openai import OpenAI
from pathlib import Path
import yaml

# load test.env file variables
from dotenv import load_dotenv
test_env = Path("test.env")
load_dotenv(test_env)

# Safety check (recommended)
if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY not found in environment")

client = OpenAI()

FEATURES_FILE = Path("features/features.yaml")
OUTPUT_FILE = Path("features/generated/build_cart.yaml")

PROMPT_TEMPLATE = """
You are a test automation expert.

Generate a Playwright test scenario in YAML using this schema:

feature:
scenario:
steps:
  - action:
    parameters:
assertions:

Available features:
{features}

Application: E-commerce site
"""


def load_features() -> dict:
    with FEATURES_FILE.open() as f:
        data = yaml.safe_load(f)
    return data["features"]


def generate_spec(features: dict, output_file: Path):
    # Turn features into readable prompt text
    feature_text = "\n".join(
        f"- {name}: {info['description']}"
        for name, info in features.items()
    )

    prompt = PROMPT_TEMPLATE.format(features=feature_text)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    yaml_content = response.choices[0].message.content
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(yaml_content)

    print(f"Spec written to {output_file}")


if __name__ == "__main__":
    features = load_features()
    # generate_spec(features, OUTPUT_FILE)

    for feature_name, feature_info in features.items():
        output_file = Path(f"features/generated/{feature_name.lower()}.yaml")
        generate_spec({feature_name: feature_info}, output_file)
