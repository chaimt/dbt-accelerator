import os
from abc import ABC

SQL = ".sql"
YML = ".yml"
MD = ".md"

home_dir = os.path.expanduser("~")
dbt_accelerator = "dbt_accelerator"
PERSIST_FOLDER = home_dir + "/." + dbt_accelerator
PERSIST_FILE = PERSIST_FOLDER + "/environment_persist.json"


PROMPT_COLOR = "#00e6e6"
HOUR_IN_SECONDS = 60 * 60
PRODUCTION_DOCS_WEB = "https://"
API_DOCS_WEB = "https://"

TARGET_USERS_DIR = "target/users"
TARGET_GIT_DIR = "target/cli"
TARGET_GIT_DIR_CACHE = "target/cli_cache"

ABORT_KEYWORD = "ABORT"
FREE_TEXT_ALLOWED_SUFFIX = " :point_right: You can use free text as well! :point_left:"
CLEAR_KEYWORD = "CLEAR"


class Logs(ABC):
    RIGHT_ARROW = ":point_right:"
    MODEL_HIGHLIGHT = "green bold"


class CLIGitRepos(ABC):
    ARTIFACTS = ""
    MASTER_BRANCH = "master"


class CLIReservedTags(ABC):
    DAG_TAG = "cli_dag"


class FolderStructure(ABC):
    PIPELINES = "pipelines"
    TRANSFORMATIONS = "transformations"


class Dbt(ABC):
    DBT_CONTAINER_NAME = "cli_dbt"
    PROFILES_FILENAME = "profiles.yml"
    DBT_PROJECT_FILE = "dbt_project.yml"


class CiCd(ABC):
    BUILD_TOOL_USER_NAME = "travis"
