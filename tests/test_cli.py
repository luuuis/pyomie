import re

from typer.testing import CliRunner

from pyomie.cli import app

runner = CliRunner()


def test_help():
    """The help message includes the CLI name."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert re.search(
        r"spot\s+Fetches the OMIE spot price data", result.stdout, flags=re.MULTILINE
    )
    assert re.search(
        r"adjustment\s+Fetches the OMIE adjustment mechanism data",
        result.stdout,
        flags=re.MULTILINE,
    )
