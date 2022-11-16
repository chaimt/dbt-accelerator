import logging
from abc import ABC

from dbt_accelerator.companion.utils import ExecutionHelper

logger = logging.getLogger(__name__)


class CompanionBase(ABC):
    def __init__(self):
        self._project_name = None

    def get_root_dir(self):
        return ExecutionHelper.get_root_dir()
