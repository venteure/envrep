import os
import re
import base64
from pathlib import Path

regular = re.compile(r'\$\((\w+)\)')
secret = re.compile(r'\$\*\((\w+)\)')


def process_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        data = file.read()

    new_data = regular.sub(lambda match: os.getenv(match.group(1), match.group(0)), data)
    new_data = secret.sub(
        lambda match: base64.b64encode(os.getenv(match.group(1), match.group(0)).encode()).decode(), new_data
    )

    with open(path, 'w', encoding='utf-8') as file:
        file.write(new_data)

    print(f"Replaced values in {path}")


def run():
    directory = os.getenv("INPUT_DIRECTORY")
    if not directory:
        raise ValueError("INPUT_DIRECTORY environment variable is not set")

    input_extensions = os.getenv("INPUT_EXTENSIONS", "yaml,yml,json,conf,hcl")
    extensions = input_extensions.split(",")
    allowed_extensions = {ext for ext in extensions}

    for ext in allowed_extensions:
        for file in Path(directory).rglob(f'*.{ext}'):
            process_file(file)


if __name__ == "__main__":
    run()
