import logging
import os

from dbt_accelerator.companion.constant import SQL, YML
from dbt_accelerator.companion.metadata.dbt_models_metadata import DomainResourceLocation, ModelType
from dbt_accelerator.companion.validations.validate_plugin import ValidatePlugin

logger = logging.getLogger(__name__)


class ModelNameValidatePlugin(ValidatePlugin):
    def is_applicable(self, file_name: str) -> bool:
        return super().is_applicable(file_name) and (file_name.endswith(SQL) or file_name.endswith(YML))

    def load_file(self, file_name: str) -> object:
        return file_name

    def validate(self, file_name: str, data: object) -> bool:
        try:
            if not file_name.startswith("models/"):
                logger.error(self.add_plugin_name_to_message(f"invalid file name {file_name}"))
                return False
            domain = file_name.split("/")[1].strip()

            model_type = ModelType.from_str(self._get_model_label(file_name))
            if model_type is None:
                logger.error(self.add_plugin_name_to_message(f"model {file_name} is not in staging or marts directory"))
                return False
            d = DomainResourceLocation(domain)
            file_prefix = d.get_model_filename_prefix(model_type)
            model_name = os.path.basename(file_name)
            if not model_name.startswith(file_prefix):
                logger.error(self.add_plugin_name_to_message(f"Model {file_name} name is not according to convention [domain_type__]."))
                return False
            if model_name.count("__") != 1:
                logger.error(self.add_plugin_name_to_message(f"Model {file_name} name is not according to convention [domain_type__]. __ can be only once"))
                return False
            return True
        except Exception as e:
            logger.error("ModelNameValidatePlugin ", e)
            return False

    def _get_model_label(self, file_name):
        label = file_name.split("/")[2].strip()
        if label == "exposures":
            return file_name.split("/")[3].strip()
        return label
