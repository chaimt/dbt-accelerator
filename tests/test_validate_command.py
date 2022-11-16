import logging
import os
import shutil
from unittest.mock import patch

import click_log
import pytest
from click.testing import CliRunner

from dbt_accelerator.click.validate import all
from dbt_accelerator.companion.utils import FileHelper
from dbt_accelerator.companion.validations.transformations.validate_model_name_plugin import ModelNameValidatePlugin
from dbt_accelerator.companion.validations.validate_command import ValidateCommand
from dbt_accelerator.companion.validations.validators import validate_all
from tests.utils import in_lines

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

click_log.basic_config(logger)

parent_dir = os.getcwd()


def mock_get_root_dir():
    return parent_dir + "/dbt_playground"


@pytest.fixture(autouse=True)
def run_around_tests():
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "DEBUG"), force=True)
    click_log.basic_config()
    yield


def test_all_no_files():
    os.environ["USER_SCHEMA"] = "dev_test"

    runner = CliRunner()
    result = runner.invoke(
        all,
        None,
    )
    assert result.exit_code == 0

    lines = result.output.split("\n")
    assert "Action: Validate all" == lines[1]


@patch("dbt_accelerator.companion.utils.ExecutionHelper.get_root_dir", mock_get_root_dir)
def test_all_playground_files(caplog):
    os.environ["USER_SCHEMA"] = "dev_test"
    os.environ["DBT_DOCKER_VERSION"] = "2.20"

    validated = validate_all("")
    lines = caplog.text.split("\n")
    assert validated
    assert in_lines(
        "[YamlExistsValidatePlugin] Validating models/example_domain/staging/base/example_domain_stg__my_first_dbt_model/example_domain_stg__my_first_dbt_model.sql",
        lines,
    )
    assert in_lines(
        "[ModelNameValidatePlugin] Validating models/example_domain/staging/base/example_domain_stg__my_first_dbt_model/example_domain_stg__my_first_dbt_model.sql",
        lines,
    )

    assert in_lines(
        "[YamlExistsValidatePlugin] Validating models/example_domain/staging/base/example_domain_stg__my_second_dbt_model/example_domain_stg__my_second_dbt_model.sql",
        lines,
    )
    assert in_lines(
        "[ModelNameValidatePlugin] Validating models/example_domain/staging/base/example_domain_stg__my_second_dbt_model/example_domain_stg__my_second_dbt_model.sql",
        lines,
    )


def test_onskip_no_models_plugin(caplog):
    filenames = "tests/test_validate_command.py"
    assert validate_all(filenames)
    lines = caplog.text.split("\n")
    assert in_lines("[YamlExistsValidatePlugin] tests/test_validate_command.py not applicable", lines)
    assert in_lines("[ModelNameValidatePlugin] tests/test_validate_command.py not applicable", lines)


@patch("dbt_accelerator.companion.utils.ExecutionHelper.get_root_dir", mock_get_root_dir)
def test_invalid_file_on_plugin(caplog):
    try:
        shutil.copyfile(f"{parent_dir}/tests/resources/bad_model.yml", f"{mock_get_root_dir()}/models/example_domain/bad_model.yml")
        filenames = "models/example_domain/exposures/scheduling/exposures.yml, models/example_domain/bad_model.yml"
        assert not validate_all(filenames)
        lines = caplog.text.split("\n")
        assert in_lines("[YamlExistsValidatePlugin] models/example_domain/exposures/scheduling/exposures.yml not applicable", lines)
        assert in_lines(
            "[ModelNameValidatePlugin] Model models/example_domain/exposures/scheduling/exposures.yml name is not according to convention [domain_type__].",
            lines,
        )

        assert in_lines("[ModelNameValidatePlugin] Validating models/example_domain/exposures/scheduling/exposures.yml", lines)
    finally:
        FileHelper.delete_file(f"{mock_get_root_dir()}/models/example_domain/bad_model.yml")


@patch("dbt_accelerator.companion.utils.ExecutionHelper.get_root_dir", mock_get_root_dir)
def test_missing_yml(caplog):
    try:
        FileHelper.create_dir(f"{mock_get_root_dir()}/models/example_domain/staging/base/example_domain_stg__bad_model")
        shutil.copyfile(
            f"{parent_dir}/tests/resources/bad_model.sql",
            f"{mock_get_root_dir()}/models/example_domain/staging/base/example_domain_stg__bad_model/example_domain_stg__bad_model.sql",
        )
        filenames = "models/example_domain/staging/base/example_domain_stg__bad_model/example_domain_stg__bad_model.sql"
        assert not validate_all(filenames)
        lines = caplog.text.split("\n")
        assert in_lines("YamlExistsValidatePlugin] Model metadata missing file for example_domain_stg__bad_model.yml", lines)
    finally:
        FileHelper.delete_dir(f"{mock_get_root_dir()}/models/example_domain/staging/base/example_domain_stg__bad_model")


@patch("dbt_accelerator.companion.utils.ExecutionHelper.get_root_dir", mock_get_root_dir)
def test_missing_md(caplog):
    try:
        FileHelper.create_dir(f"{mock_get_root_dir()}/models/example_domain/staging/base/example_domain_stg__bad_model")
        shutil.copyfile(
            f"{parent_dir}/tests/resources/bad_model.sql",
            f"{mock_get_root_dir()}/models/example_domain/staging/base/example_domain_stg__bad_model/example_domain_stg__bad_model.sql",
        )
        shutil.copyfile(
            f"{parent_dir}/tests/resources/bad_model.yml",
            f"{mock_get_root_dir()}/models/example_domain/staging/base/example_domain_stg__bad_model/example_domain_stg__bad_model.yml",
        )
        filenames = "models/example_domain/staging/base/example_domain_stg__bad_model/example_domain_stg__bad_model.sql"
        assert not validate_all(filenames)
        lines = caplog.text.split("\n")
        assert in_lines("[YamlExistsValidatePlugin] Model document missing file for example_domain_stg__bad_model.md", lines)
    finally:
        FileHelper.delete_dir(f"{mock_get_root_dir()}/models/example_domain/staging/base/example_domain_stg__bad_model")


@patch("dbt_accelerator.companion.utils.ExecutionHelper.get_root_dir", mock_get_root_dir)
def test_model_name_plugin(caplog):
    filenames = """
        models/platform/staging/marts_compatible/platform_stg__stores_enrichment.yml,
        models/platform/staging/marts_compatible/platform_stg__stores_enrichment.sql,
        models/platform/staging/base/platform_stg__stores.yml"""
    assert ValidateCommand().validate_files(filenames, [ModelNameValidatePlugin()])
    lines = caplog.text.split("\n")
    assert in_lines(
        "[ModelNameValidatePlugin] Validating models/platform/staging/marts_compatible/platform_stg__stores_enrichment.yml",
        lines,
    )
    assert in_lines(
        "[ModelNameValidatePlugin] Validating models/platform/staging/marts_compatible/platform_stg__stores_enrichment.sql",
        lines,
    )
    assert in_lines(
        "[ModelNameValidatePlugin] Validating models/platform/staging/base/platform_stg__stores.yml",
        lines,
    )


@patch("dbt_accelerator.companion.utils.ExecutionHelper.get_root_dir", mock_get_root_dir)
def test_model_name_plugin_for_source(caplog):
    filenames = "models/example_domain/source/example_domain__src.yml"
    assert ValidateCommand().validate_files(filenames, [ModelNameValidatePlugin()])
    lines = caplog.text.split("\n")
    assert in_lines(
        "[ModelNameValidatePlugin] Validating models/example_domain/source/example_domain__src.yml",
        lines,
    )


@patch("dbt_accelerator.companion.utils.ExecutionHelper.get_root_dir", mock_get_root_dir)
def test_model_name_plugin_for_source_wrong_domain(caplog):
    filenames = "models/example_domain/source/loyalty__src.yml"
    assert not ValidateCommand().validate_files(filenames, [ModelNameValidatePlugin()])
    lines = caplog.text.split("\n")
    assert in_lines(
        "[ModelNameValidatePlugin] Model models/example_domain/source/loyalty__src.yml name is not according to convention [domain_type__].",
        lines,
    )


@patch("dbt_accelerator.companion.utils.ExecutionHelper.get_root_dir", mock_get_root_dir)
def test_file_name_underscore_plugin_error(caplog):
    filenames = "models/platform/staging/marts_compatible/platform__platform_stg__stores_enrichment.yml"
    assert not ValidateCommand().validate_files(filenames, [ModelNameValidatePlugin()])

    filenames = "models/platform/staging/marts_compatible/platform__platform_stg__stores_enrichment.sql"
    assert not ValidateCommand().validate_files(filenames, [ModelNameValidatePlugin()])
    lines = caplog.text.split("\n")
    assert in_lines(
        "[ModelNameValidatePlugin] Model models/platform/staging/marts_compatible/platform__platform_stg__stores_enrichment.yml "
        "name is not according to convention [domain_type__].",
        lines,
    )
    assert in_lines(
        "[ModelNameValidatePlugin] Model models/platform/staging/marts_compatible/platform__platform_stg__stores_enrichment.sql "
        "name is not according to convention [domain_type__].",
        lines,
    )


@patch("dbt_accelerator.companion.utils.ExecutionHelper.get_root_dir", mock_get_root_dir)
def test_exposure_name_underscore_plugin_error(caplog):
    filenames = "models/platform/exposures/scheduling/platform__platform__stores_enrichment.yml"
    assert not ValidateCommand().validate_files(filenames, [ModelNameValidatePlugin()])
    lines = caplog.text.split("\n")
    assert in_lines(
        "[ModelNameValidatePlugin] Model models/platform/exposures/scheduling/platform__platform__stores_enrichment.yml "
        "name is not according to convention [domain_type__]. __ can be only once",
        lines,
    )


def test_invalid_model_path_plugin(caplog):
    filenames = """start/models/platform/staging/marts_compatible/platform_stg__stores_enrichment.yml,
    start/models/platform/staging/marts_compatible/platform_stg__stores_enrichment.sql,
    models/platform/staging/base/platform_stg__stores.yml"""
    assert not ValidateCommand().validate_files(filenames, [ModelNameValidatePlugin()])
    assert "[ModelNameValidatePlugin] invalid file name start/models/platform/staging/marts_compatible/platform_stg__stores_enrichment.yml" in caplog.text


def test_invalid_model_type_path_plugin(caplog):
    filenames = """models/platform/staging_1/marts_compatible/platform_stg__stores_enrichment.yml,
    models/platform/staging_1/marts_compatible/platform_stg__stores_enrichment.sql,
    models/platform/staging/base/platform_stg__stores.yml"""
    assert not ValidateCommand().validate_files(filenames, [ModelNameValidatePlugin()])
    assert "is not in staging or marts directory" in caplog.text


def test_model_name_invalid_name_plugin(caplog):
    filenames = """models/platform/staging/marts_compatible/platform_stg__stores_enrichment.yml,
    models/platform/staging/marts_compatible/platform__stores_enrichment.sql,
    models/platform/staging/base/platform__stores.yml"""
    assert not ValidateCommand().validate_files(filenames, [ModelNameValidatePlugin()])
    assert "Model models/platform/staging/marts_compatible/platform__stores_enrichment.sql name is not according to convention [domain_type__]." in caplog.text
