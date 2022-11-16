import click
import pytest
from click.testing import CliRunner

from dbt_accelerator.click.decorators.option_decorators import dry_run_option, filenames_option, trace_option
from dbt_accelerator.click.log_decorators import wrap_action
from dbt_accelerator.click.log_handlers import setup_log


@pytest.fixture(autouse=True)
def run_around_tests():
    setup_log("DEBUG")
    yield


@click.command()
@trace_option()
@dry_run_option()
def trace_be_decorated(trace: bool, dry_run: bool):
    click.echo(f"trace: {str(trace)}, dry_run: {str(dry_run)}")


def test_trace_option_help():
    runner = CliRunner()
    result = runner.invoke(trace_be_decorated, ["--help"])
    assert result.exit_code == 0
    assert "Usage: trace-be-decorated [OPTIONS]" in result.output
    assert "-t, --trace     Enable :point_right: [yellow]debug mode[/] :point_left:" in result.output


def test_trace_option():
    runner = CliRunner()
    result = runner.invoke(trace_be_decorated, ["--trace"])
    assert result.exit_code == 0
    assert result.output == "trace: True, dry_run: False\n"

    result = runner.invoke(trace_be_decorated, ["--trace", "--dry-run"])
    assert result.exit_code == 0
    assert result.output == "trace: True, dry_run: True\n"


@click.command()
@wrap_action("abc")
def wrap_action_be_decorated():
    click.echo("ran wrap_action_be_decorated")


def test_wrap_action_be_decorated(caplog):
    runner = CliRunner()
    result = runner.invoke(wrap_action_be_decorated, [])
    assert result.exit_code == 0
    assert "ran wrap_action_be_decorated\n" in result.output
    assert "Action: abc\n" in caplog.text


@click.command()
@filenames_option()
def filenames_option_be_decorated(filenames):
    click.echo("ran filenames_option_be_decorated " + filenames)


def test_filenames_option_be_decorated(caplog):
    runner = CliRunner()
    result = runner.invoke(filenames_option_be_decorated, ["--filenames", "test"])
    assert result.exit_code == 0
    assert "ran filenames_option_be_decorated test\n" in result.output
