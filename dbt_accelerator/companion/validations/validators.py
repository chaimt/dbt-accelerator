import logging

from dbt_accelerator.companion.validations.transformations.validate_model_name_plugin import ModelNameValidatePlugin
from dbt_accelerator.companion.validations.transformations.validate_yaml_exists_plugin import YamlExistsValidatePlugin
from dbt_accelerator.companion.validations.validate_command import ValidateCommand

logger = logging.getLogger(__name__)


def validate_all(filenames: str) -> int:
    try:
        return ValidateCommand().validate_files(
            filenames,
            [
                YamlExistsValidatePlugin(),
                ModelNameValidatePlugin(),
                # ModelValidatePlugin(),
                # ExposureValidatePlugin(),
                # SourceValidatePlugin(),
                # ValidateSqlSyntaxPlugin(),
            ],
        )
    except Exception as e:
        logger.error(e)
        return -1
