from abc import ABC, abstractmethod

from dbt_accelerator.companion.utils import ExecutionHelper


class ValidatePlugin(ABC):
    def get_full_file_name(self, filename: str):
        full_filename = filename
        if not full_filename.startswith(ExecutionHelper.get_root_dir()):
            full_filename = ExecutionHelper.get_root_dir() + "/" + filename
        return full_filename

    @abstractmethod
    def is_applicable(self, file_name: str) -> bool:
        return "models/" in file_name

    @abstractmethod
    def load_file(self, file_name: str) -> object:
        pass

    @abstractmethod
    def validate(self, file_name: str, data: object) -> bool:
        pass

    def add_plugin_name_to_message(self, message):
        return f"[{type(self).__name__}] {message}"
