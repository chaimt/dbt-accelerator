import pytest
from click.testing import CliRunner

from dbt_accelerator.click.cli import version
from dbt_accelerator.click.log_handlers import setup_log
from tests.utils import in_lines


@pytest.fixture(autouse=True)
def run_around_tests():
    setup_log("DEBUG")
    yield


def test_version(caplog):
    runner = CliRunner()

    result = runner.invoke(
        version,
        [],
    )
    assert result.exit_code == 0
    assert "DBT info:" in caplog.text
    lines = result.output.split("\n")
    assert in_lines("DBT info:", lines)
