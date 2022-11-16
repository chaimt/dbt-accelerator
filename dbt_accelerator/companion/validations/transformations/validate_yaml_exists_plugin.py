import logging
import os

from dbt_accelerator.companion.constant import MD, SQL, YML
from dbt_accelerator.companion.validations.transformations.validate_sql_plugin import ValidateSqlPlugin

logger = logging.getLogger(__name__)


class YamlExistsValidatePlugin(ValidateSqlPlugin):
    def validate(self, file_name: str, data: object) -> bool:
        try:
            yml_filename = self.get_full_file_name(file_name.strip().replace(SQL, YML))
            if not os.path.exists(yml_filename):
                file_name = os.path.basename(yml_filename.replace("\\", os.sep))
                logger.error(self.add_plugin_name_to_message(f"Model metadata missing file for {file_name}"))
                file_name.replace(SQL, "")
                # logger.info(f"run: dbt_accelerator model field-enhance -m {model_name}")
                return False
            md_filename = self.get_full_file_name(file_name.strip().replace(SQL, MD))
            if not os.path.exists(md_filename):
                file_name = os.path.basename(md_filename.replace("\\", os.sep))
                logger.error(self.add_plugin_name_to_message(f"Model document missing file for {file_name}"))
                return False
            return True
        except Exception as e:
            logger.error("YamlExistsValidatePlugin ", e)
            return False
