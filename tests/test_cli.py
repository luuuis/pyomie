import re

import pytest
from typer.testing import CliRunner

from pyomie.cli import app

runner = CliRunner()


@pytest.mark.skip("Passing locally but failing in CI")
def test_help():
    """The help message includes the CLI name."""
    res = runner.invoke(app, ["--help"])
    assert res.exit_code == 0

    help = res.stdout
    assert re.search(r"spot\s+Fetches the OMIE spot price data", help)
