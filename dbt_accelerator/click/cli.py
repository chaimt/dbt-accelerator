#!/usr/bin/env python3
import logging
import os
import sys
import traceback

import rich_click as click
from click_plugins import with_plugins
from pkg_resources import iter_entry_points
from rich.prompt import Prompt

from dbt_accelerator.click.ci_cd_task.cidd import cicd
from dbt_accelerator.click.decorators.option_decorators import dry_run_option, trace_option
from dbt_accelerator.click.log_decorators import wrap_action
from dbt_accelerator.click.log_handlers import log_to_file_logger, setup_log, stream_handler
from dbt_accelerator.click.prompt_utils import PromptUtils, prompt_kwargs, setup_repl
from dbt_accelerator.click.validate import CLI_VALIDATE_COMMAND_GROUPS, validate
from dbt_accelerator.click.warehouse import CLI_WAREHOUSE_COMMAND_GROUPS, warehouse
from dbt_accelerator.companion.constant import PERSIST_FOLDER
from dbt_accelerator.companion.utils import FileHelper


# Use Rich markup
click.rich_click.USE_RICH_MARKUP = True

CLI_COMMAND_GROUPS = [
    {
        "name": "Main usage",
        "commands": ["create", "fetch", "run", "test", "view", "docs", "export", "clean", "repl", "exit"],
    },
    {
        "name": "Advanced usage",
        "commands": ["databricks", "dbt", "validate", "show-advanced", "warehouse", "git"],
    },
    {
        "name": "Configuration",
        "commands": ["env", "use", "version"],
    },
]

click.rich_click.COMMAND_GROUPS = {
    "dbt_accelerator": CLI_COMMAND_GROUPS,
    "dbt_accelerator ": CLI_COMMAND_GROUPS,
    "dbt_accelerator validate": CLI_VALIDATE_COMMAND_GROUPS,
    "dbt_accelerator  validate": CLI_VALIDATE_COMMAND_GROUPS,
    "dbt_accelerator warehouse": CLI_WAREHOUSE_COMMAND_GROUPS,
    "dbt_accelerator  warehouse": CLI_WAREHOUSE_COMMAND_GROUPS,
}

logger = logging.getLogger(__name__)


@click.command(help="Exit")
@wrap_action("Exit")
def exit():
    """Exit"""
    os._exit(0)


@click.command(help="View git documentation")
@wrap_action("View Documentation")
def documentation():
    """View git documentation"""
    click.launch("https://location.to.docs/")


@click.command()
def repl():
    """Start an interactive session."""

    logger.info(PromptUtils.color_text(r"██████╗ ██╗ ██████╗ ██████╗  █████╗ ███╗   ██╗██████╗  █████╗ ", "dark_green"))
    logger.info(PromptUtils.color_text(r"██╔══██╗██║██╔════╝ ██╔══██╗██╔══██╗████╗  ██║██╔══██╗██╔══██╗", "dark_green"))
    logger.info(PromptUtils.color_text(r"██████╔╝██║██║  ███╗██████╔╝███████║██╔██╗ ██║██║  ██║███████║", "dark_green"))
    logger.info(PromptUtils.color_text(r"██╔══██╗██║██║   ██║██╔═══╝ ██╔══██║██║╚██╗██║██║  ██║██╔══██║", "dark_green"))
    logger.info(PromptUtils.color_text(r"██████╔╝██║╚██████╔╝██║     ██║  ██║██║ ╚████║██████╔╝██║  ██║", "dark_green"))
    logger.info(PromptUtils.color_text(r"╚═════╝ ╚═╝ ╚═════╝ ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝", "dark_green"))

    logger.info("\n\n")

    setup_repl()


@click.command(help="Clean dbt packages and target folder")
@wrap_action("Clean")
def clean():
    """Clean dbt packages and target folder"""


@click.command(help="""View components versions""")
@wrap_action("Version")
def version():
    """View components versions"""
    logger.info("DBT info:")


@click.command(help="""Show cli history commands""")
@click.option("-l", "--limit", default=-1, help="History Limit", type=int)
def history(limit: int):
    """Show cli history commands"""
    history_lines = prompt_kwargs["history"].get_strings()
    count_lines = 0
    for line in history_lines:
        count_lines = count_lines + 1
        if limit != -1 and count_lines > limit:
            break
        click.echo(line)


def setup_log_config(trace):
    if trace:
        setup_log("DEBUG")
    else:
        setup_log("INFO")


@with_plugins(iter_entry_points("click_command_tree"))
@click.group()
@trace_option()
@dry_run_option()
def cli(trace, dry_run):
    if not FileHelper.file_exists(PERSIST_FOLDER):
        FileHelper.create_dir(PERSIST_FOLDER)

    os.environ["CLI_RUNNING"] = "True"
    setup_log_config(trace)
    # load_configuration(dry_run)
    # load_environment()


def enable_ci_cd_mode():
    cli.add_command(cicd)
    logger.info("Enabled CI CD mode.")


cli.add_command(history)
cli.add_command(version)
cli.add_command(validate)
cli.add_command(repl)
cli.add_command(exit)
cli.add_command(warehouse)


try:
    if os.environ["CI_CD_MODE"] == "True":
        enable_ci_cd_mode()

except Exception:
    pass


def log_exception(exc_type, exc_value, exc_traceback):
    """handle all exceptions"""
    filename, line, dummy, dummy = traceback.extract_tb(exc_traceback).pop()
    filename = os.path.basename(filename)
    error = "%s: %s" % (exc_type.__name__, exc_value)
    logger.error(":woman_facepalming: " + error)
    logger.error(f"filename: {filename} : {line}")
    logger.error(traceback.format_exc())
    Prompt.ask("Press key to exit.")


# install handler for exceptions
sys.excepthook = log_exception


def loop_repl():
    try:
        # InteractiveGuiFactory().register(ClickInteractiveGui())
        # EnvironmentConfig().notifiers.clear()
        # EnvironmentConfig().notifiers.append(UserCompanion())
        cli.main(standalone_mode=False)
    except SystemExit as e:
        if e.code == 0:
            logger.info(f"Process Exited {e.code}")
        else:
            logger.error(f"Process Exited {e.code}")
        sys.exit(e.code)
    except BaseException as e:
        # if EnvironmentConfig().state.error_count == 0:
        #     EnvironmentConfig().state.error_time = datetime.now()
        # diff = datetime.now() - EnvironmentConfig().state.error_time
        # if diff.total_seconds() > 60:
        #     EnvironmentConfig().state.error_count = 0
        # EnvironmentConfig().state.error_count = EnvironmentConfig().state.error_count + 1
        log_to_file_logger.error(e, exc_info=True)
        sys.exit(1)
        # if EnvironmentConfig().state.error_count > 10:
        #     logger.error("More than 10 consecutive errors in one minute")
        # elif EnvironmentConfig().in_repl:
        #     cli.add_command(repl)
        #     loop_repl()
        # else:
        #     sys.exit(1)


if __name__ == "__main__":
    loop_repl()
