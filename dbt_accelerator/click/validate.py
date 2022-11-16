import logging

import rich_click as click

from dbt_accelerator.click.decorators.option_decorators import filenames_option
from dbt_accelerator.click.log_decorators import wrap_action
from dbt_accelerator.companion.validations.transformations.validate_model_name_plugin import ModelNameValidatePlugin
from dbt_accelerator.companion.validations.transformations.validate_yaml_exists_plugin import YamlExistsValidatePlugin
from dbt_accelerator.companion.validations.validate_command import ValidateCommand
from dbt_accelerator.companion.validations.validators import validate_all

logger = logging.getLogger(__name__)

CLI_VALIDATE_COMMAND_GROUPS = [
    {
        "name": "Main usage",
        "commands": ["all"],
    },
    {
        "name": "Advanced usage",
        "commands": ["freshness"],
    },
]


@click.command(help="Execute freshness validations")
@filenames_option()
@wrap_action("Validate freshness")
def freshness(filenames):
    """Execute freshness validations"""
    if ValidateCommand().validate_files(filenames, []):
        logger.info("All files are valid.")


# @click.command(help="Execute exposures validations")
# @filenames_option()
# @wrap_action("Validate exposures")
# def exposures(filenames):
#     """Execute exposures validations"""
#     if ValidateCommand().validate_files(filenames, [ExposureValidatePlugin()]):
#         logger.info("All files are valid.")


# @click.command(help="Execute sources validations")
# @filenames_option()
# @wrap_action("Validate sources")
# def sources(filenames):
#     """Execute sources validations"""
#     if ValidateCommand().validate_files(filenames, [SourceValidatePlugin()]):
#         logger.info("All source files are valid.")


@click.command(help="Execute model metadata exists validation")
@filenames_option()
@wrap_action("Validate Yaml Exists")
def yaml_exists(filenames):
    """Execute model metadata exists validation"""
    if ValidateCommand().validate_files(filenames, [YamlExistsValidatePlugin()]):
        logger.info("All YML files are valid.")


@click.command(help="Execute model namings validations")
@filenames_option()
@wrap_action("Validate model names")
def model_name(filenames):
    """Execute model namings validations"""
    if ValidateCommand().validate_files(filenames, [ModelNameValidatePlugin()]):
        logger.info("All model files are valid.")


# @click.command(help="Execute sql syntax validations")
# @filenames_option()
# @wrap_action("Validate sql syntax")
# def sql_syntax(filenames):
#     """Execute sql syntax validations"""
#     if ValidateCommand().validate_files(filenames, [ValidateSqlSyntaxPlugin()]):
#         logger.info("All SQL syntax files are valid.")


@click.command(help="Execute all existing validations")
@filenames_option()
@wrap_action("Validate all")
def all(filenames):
    """Execute all existing validations"""
    if validate_all(filenames):
        logger.info("All files are valid.")


@click.group(help="Commands for configuration validation")
def validate():
    """Commands for configuration validation"""


validate.add_command(all)
validate.add_command(model_name)
# validate.add_command(sql_syntax)
validate.add_command(yaml_exists)
# validate.add_command(freshness)
# validate.add_command(exposures)
# validate.add_command(sources)
