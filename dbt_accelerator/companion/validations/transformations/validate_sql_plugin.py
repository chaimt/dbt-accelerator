from dbt_accelerator.companion.constant import SQL
from dbt_accelerator.companion.validations.validate_plugin import ValidatePlugin


class ValidateSqlPlugin(ValidatePlugin):
    def is_applicable(self, file_name: str) -> bool:
        return super().is_applicable(file_name) and file_name.endswith(SQL)

    def load_file(self, file_name: str) -> object:
        return file_name
