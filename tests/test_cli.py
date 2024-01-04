from typer.testing import CliRunner

from pyomie.cli import app

runner = CliRunner()


def test_help():
    """The help message includes the CLI name."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Add the arguments and print the result" in result.stdout