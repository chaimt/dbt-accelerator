import logging
import os
from argparse import ArgumentError
from enum import Enum

from dbt_accelerator.companion.constant import YML
from dbt_accelerator.companion.utils import ExecutionHelper, FileHelper

logger = logging.getLogger(__name__)


class SuperEnum(Enum):
    @classmethod
    def to_dict(cls):
        """Returns a dictionary representation of the enum."""
        return {e.name: e.value for e in cls}

    @classmethod
    def keys(cls):
        """Returns a list of all the enum keys."""
        return cls._member_names_

    @classmethod
    def values(cls):
        """Returns a list of all the enum values."""
        return list(cls._value2member_map_.keys())

    def __str__(self):
        return self.value.capitalize()


class ModelType(SuperEnum):
    SOURCE = "Model - Source"
    BASE = "Model - Base"
    STAGING = "Model - Staging"
    MARTS = "Model - Marts"
    SCHEDULING_EXPOSURES = "scheduling_exposures"

    @staticmethod
    def get_exposures() -> list:
        return [ModelType.SCHEDULING_EXPOSURES]

    @staticmethod
    def get_model_valid_types_values():
        return [model_type.value for model_type in ModelType.get_model_valid_types()]

    @staticmethod
    def get_model_valid_types():
        return [
            ModelType.BASE,
            ModelType.STAGING,
            ModelType.MARTS,
        ]

    @staticmethod
    def from_str(label):
        lower_label = label.lower()
        if lower_label in [ModelType.SOURCE.name.lower(), ModelType.SOURCE.value.lower()]:
            return ModelType.SOURCE
        elif lower_label in [ModelType.BASE.name.lower(), ModelType.BASE.value.lower()]:
            return ModelType.BASE
        elif lower_label in [ModelType.STAGING.name.lower(), ModelType.STAGING.value.lower()]:
            return ModelType.STAGING
        elif lower_label in [ModelType.MARTS.name.lower(), ModelType.MARTS.value.lower()]:
            return ModelType.MARTS
        elif lower_label in [
            ModelType.SCHEDULING_EXPOSURES.name.lower(),
            ModelType.SCHEDULING_EXPOSURES.value.lower(),
            "scheduling",
        ]:
            return ModelType.SCHEDULING_EXPOSURES


class DomainResourceLocation(object):
    def __init__(self, domain):
        self.domain = domain

    def get_doc_dir(self):
        doc_file = f"{ExecutionHelper.get_root_dir()}/docs/{self.domain}.md"
        doc_file_exists = os.path.exists(doc_file)
        FileHelper.touch(doc_file)
        if doc_file_exists:
            logger.info(f"Docs file {doc_file} Updated. :white_heavy_check_mark:")
        else:
            logger.info(f"Docs file {doc_file} Created. :white_check_mark:")
        return doc_file

    def get_model_dir_by_type(self, type: ModelType) -> str:
        if type == ModelType.SOURCE:
            return f"{ExecutionHelper.get_root_dir()}/models/{self.domain}/source/"
        elif type == ModelType.BASE:
            return f"{ExecutionHelper.get_root_dir()}/models/{self.domain}/staging/base/"
        elif type == ModelType.STAGING:
            return f"{ExecutionHelper.get_root_dir()}/models/{self.domain}/staging/marts_compatible/"
        elif type == ModelType.MARTS:
            return f"{ExecutionHelper.get_root_dir()}/models/{self.domain}/marts/"
        elif type == ModelType.SCHEDULING_EXPOSURES:
            return f"{ExecutionHelper.get_root_dir()}/models/{self.domain}/exposures/scheduling"
        else:
            raise ArgumentError(f"Invalid model type given: {type}.")

    def get_exposure_dir(self, model_type: ModelType) -> str:
        return f"{ExecutionHelper.get_root_dir()}/models/{self.domain}/exposures/{'scheduling/' if model_type == ModelType.SCHEDULING_EXPOSURES else 'looker/' }"

    def get_model_filename_prefix(self, type: ModelType):
        if type == ModelType.STAGING or type == ModelType.BASE:
            return f"{self.domain}_stg__"
        elif type == ModelType.MARTS or type in ModelType.get_exposures() or type == ModelType.SOURCE:
            return f"{self.domain}__"
        else:
            raise ArgumentError(f"Invalid model type given: {type}.")

    def get_model_name(self, model_name: str, type: ModelType):
        if model_name.startswith(f"{self.domain}_"):
            return model_name
        model_filename_prefix = self.get_model_filename_prefix(type)
        return f"{model_filename_prefix}{model_name}"

    def get_model_filename(self, model_name: str, type: ModelType, full_path: bool = False):
        if not full_path:
            return f"{self.get_model_name(model_name, type)}.sql"
        dir_prefix = self.get_model_dir_by_type(type)
        full_model_name = self.get_model_name(model_name, type)
        return f"{dir_prefix}{full_model_name}/{full_model_name}.sql"

    def get_exposure_filename(self, exposure_name: str, model_type: ModelType):
        name = f"{exposure_name}{YML}" if exposure_name.startswith(self.domain) else f"{self.domain}__{exposure_name}{YML}"
        return f"{self.get_exposure_dir(model_type)}{name}"

    def get_model_source_filename(self, full_path: bool = False):
        dir_prefix = "" if not full_path else self.get_model_dir_by_type(ModelType.SOURCE)
        return f"{dir_prefix}{self.domain}__src.yml"

    def get_model_metadata_filename(self, model_name: str, type: ModelType, full_path: bool = False):
        if not full_path:
            return f"{self.get_model_name(model_name, type)}.yml"
        dir_prefix = self.get_model_dir_by_type(type)
        full_model_name = self.get_model_name(model_name, type)
        return f"{dir_prefix}{full_model_name}/{full_model_name}.yml"

    def get_model_documentation_filename(self, model_name: str, type: ModelType, full_path: bool = False):
        if type == ModelType.SOURCE:
            return f"{ExecutionHelper.get_root_dir()}/docs/{self.domain}.md"
        else:
            dir_prefix = "" if not full_path else self.get_model_dir_by_type(type)
            full_model_name = self.get_model_name(model_name, type)
            return f"{dir_prefix}{full_model_name}/{full_model_name}.md"
