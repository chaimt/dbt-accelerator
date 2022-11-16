import logging
import os
import shutil

from dbt_accelerator.companion.constant import Dbt, FolderStructure

logger = logging.getLogger(__name__)


class ExecutionHelper:
    @staticmethod
    def get_root_dir():
        if os.path.exists(Dbt.DBT_PROJECT_FILE):
            return os.getcwd()
        elif os.path.exists(f"{os.getcwd()}/{FolderStructure.TRANSFORMATIONS}/{Dbt.DBT_PROJECT_FILE}"):
            return f"{os.getcwd()}/{FolderStructure.TRANSFORMATIONS}"
        else:
            raise Exception("Running from an unknown directory")


class FileHelper(object):
    @staticmethod
    def file_exists(full_file_path: str) -> bool:
        return os.path.exists(full_file_path)

    @staticmethod
    def create_dir(dir_path: str, exists_ok: bool = True) -> None:
        os.makedirs(dir_path, exist_ok=exists_ok)

    @staticmethod
    def delete_dir(dir_path: str) -> None:
        shutil.rmtree(dir_path, ignore_errors=True)

    @staticmethod
    def delete_file(file_path: str, missing_ok: bool = True) -> None:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Deleted {file_path}")
        else:
            if missing_ok:
                return
            logger.debug(f"File {file_path} does not exist.")

    @staticmethod
    # Touch will create file if it does not exist
    def touch(path: str, template_name: str = None):
        basedir = os.path.dirname(path)
        if not os.path.exists(basedir):
            os.makedirs(basedir)
