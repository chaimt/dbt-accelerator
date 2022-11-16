import logging
import pathlib
from typing import List

from dbt_accelerator.companion.common_companion import CompanionBase
from dbt_accelerator.companion.constant import SQL, YML
from dbt_accelerator.companion.utils import ExecutionHelper
from dbt_accelerator.companion.validations.validate_plugin import ValidatePlugin

logger = logging.getLogger(__name__)


class ValidateCommand(CompanionBase):
    def fill_names_if_empty(self, filenames: str) -> str:
        if not filenames:
            path = ExecutionHelper.get_root_dir() + "/models"
            files = (p.resolve() for p in pathlib.Path(path).glob("**/*") if p.suffix in {YML, SQL})
            filenames = []
            for config_file in files:
                filenames.append((str(config_file)).replace(ExecutionHelper.get_root_dir() + "/", ""))
            filenames = ",".join(filenames)
        return filenames

    def validate_files(self, filenames: str, validators: List[ValidatePlugin]) -> bool:
        filenames = self.fill_names_if_empty(filenames)
        filenames_list = filenames.split(",")
        for filename in filenames_list:
            filename = filename.strip()
            for validator in validators:
                if validator.is_applicable(filename):
                    logger.debug(validator.add_plugin_name_to_message(f"Validating {filename}"))
                    data = validator.load_file(filename)
                    if data and not validator.validate(filename, data):
                        return False
                else:
                    logger.debug(validator.add_plugin_name_to_message(f"{filename} not applicable"))
        return True
