import re

from typer.testing import CliRunner

from pyomie.cli import app

runner = CliRunner()


def test_help():
    """The help message includes the CLI name."""
    res = runner.invoke(app, ["--help"])
    assert res.exit_code == 0

    help_text = res.stdout
    assert re.search(r"Fetch the OMIE spot price data", help_text)
