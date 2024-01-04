import subprocess
import sys


def test_can_run_as_python_module():
    """Run the CLI as a Python module."""
    result = subprocess.run(
        [sys.executable, "-m", "pyomie", "--help"],  # noqa S603,S607
        check=True,
        capture_output=True,
    )
    assert result.returncode == 0
    assert b"pyomie [OPTIONS]" in result.stdout