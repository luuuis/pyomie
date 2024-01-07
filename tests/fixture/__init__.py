import os

_FIXTURES_DIR = os.path.dirname(os.path.realpath(__file__))


def read_file(filename: str) -> str:
    with open(os.path.join(_FIXTURES_DIR, filename)) as file:
        return file.read()
