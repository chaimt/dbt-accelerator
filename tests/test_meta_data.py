import os
from unittest.mock import patch

from dbt_accelerator.companion.metadata.dbt_models_metadata import DomainResourceLocation, ModelType

parent_dir = os.getcwd()
if "/tools/cli" not in parent_dir:
    parent_dir = parent_dir + "/tools/cli"


def mock_get_root_dir():
    return parent_dir + "/dbt_playground"


def test_ModelType_from_str():
    assert ModelType.from_str("SOURCE") == ModelType.SOURCE
    assert ModelType.from_str("Model - Source") == ModelType.SOURCE

    assert ModelType.from_str("BASE") == ModelType.BASE
    assert ModelType.from_str("Model - Base") == ModelType.BASE

    assert ModelType.from_str("STAGING") == ModelType.STAGING
    assert ModelType.from_str("Model - Staging") == ModelType.STAGING

    assert ModelType.from_str("MARTS") == ModelType.MARTS
    assert ModelType.from_str("Model - Marts") == ModelType.MARTS

    assert ModelType.from_str("SCHEDULING_EXPOSURES") == ModelType.SCHEDULING_EXPOSURES
    assert ModelType.from_str("scheduling_exposures") == ModelType.SCHEDULING_EXPOSURES


def test_get_model_valid_types():
    assert ModelType.get_model_valid_types() == [ModelType.BASE, ModelType.STAGING, ModelType.MARTS]


@patch("dbt_accelerator.companion.utils.ExecutionHelper.get_root_dir", mock_get_root_dir)
def test_get_model_dir_by_type():
    domain_resource_location = DomainResourceLocation("example_domain")
    assert domain_resource_location.get_model_dir_by_type(ModelType.BASE).endswith("models/example_domain/staging/base/")
    assert domain_resource_location.get_model_dir_by_type(ModelType.STAGING).endswith("models/example_domain/staging/marts_compatible/")
    assert domain_resource_location.get_model_dir_by_type(ModelType.MARTS).endswith("models/example_domain/marts/")
    assert domain_resource_location.get_model_dir_by_type(ModelType.SCHEDULING_EXPOSURES).endswith("models/example_domain/exposures/scheduling")


def test_get_model_name():
    domain_resource_location = DomainResourceLocation("example_domain")
    assert domain_resource_location.get_model_name("model1", ModelType.BASE) == "example_domain_stg__model1"
    assert domain_resource_location.get_model_name("model1", ModelType.STAGING) == "example_domain_stg__model1"
    assert domain_resource_location.get_model_name("model1", ModelType.MARTS) == "example_domain__model1"


def test_get_model_filename_prefix():
    domain_resource_location = DomainResourceLocation("example_domain")
    assert domain_resource_location.get_model_filename_prefix(ModelType.BASE) == "example_domain_stg__"
    assert domain_resource_location.get_model_filename_prefix(ModelType.STAGING) == "example_domain_stg__"
    assert domain_resource_location.get_model_filename_prefix(ModelType.MARTS) == "example_domain__"
    assert domain_resource_location.get_model_filename_prefix(ModelType.SCHEDULING_EXPOSURES) == "example_domain__"


@patch("dbt_accelerator.companion.utils.ExecutionHelper.get_root_dir", mock_get_root_dir)
def test_get_model_source_filename():
    domain_resource_location = DomainResourceLocation("example_domain")
    assert domain_resource_location.get_model_source_filename(True).endswith("dbt_playground/models/example_domain/source/example_domain__src.yml")
    assert domain_resource_location.get_model_source_filename(False) == "example_domain__src.yml"


@patch("dbt_accelerator.companion.utils.ExecutionHelper.get_root_dir", mock_get_root_dir)
def test_get_model_filename():
    domain_resource_location = DomainResourceLocation("example_domain")
    assert domain_resource_location.get_model_filename("model1", ModelType.BASE, True).endswith(
        "models/example_domain/staging/base/example_domain_stg__model1/example_domain_stg__model1.sql"
    )
    assert domain_resource_location.get_model_filename("model1", ModelType.BASE, False) == "example_domain_stg__model1.sql"

    assert domain_resource_location.get_model_filename("model1", ModelType.STAGING, True).endswith(
        "models/example_domain/staging/marts_compatible/example_domain_stg__model1/example_domain_stg__model1.sql"
    )
    assert domain_resource_location.get_model_filename("model1", ModelType.STAGING, False) == "example_domain_stg__model1.sql"

    assert domain_resource_location.get_model_filename("model1", ModelType.MARTS, True).endswith(
        "models/example_domain/marts/example_domain__model1/example_domain__model1.sql"
    )
    assert domain_resource_location.get_model_filename("model1", ModelType.MARTS, False) == ("example_domain__model1.sql")


@patch("dbt_accelerator.companion.utils.ExecutionHelper.get_root_dir", mock_get_root_dir)
def test_get_exposure_filename():
    domain_resource_location = DomainResourceLocation("example_domain")
    assert domain_resource_location.get_exposure_filename("exposure1", ModelType.SCHEDULING_EXPOSURES).endswith(
        "models/example_domain/exposures/scheduling/example_domain__exposure1.yml"
    )
    assert domain_resource_location.get_exposure_filename("example_domain__exposure1", ModelType.SCHEDULING_EXPOSURES).endswith(
        "models/example_domain/exposures/scheduling/example_domain__exposure1.yml"
    )


@patch("dbt_accelerator.companion.utils.ExecutionHelper.get_root_dir", mock_get_root_dir)
def test_get_model_metadata_filename():
    domain_resource_location = DomainResourceLocation("example_domain")
    assert domain_resource_location.get_model_metadata_filename("model1", ModelType.BASE, True).endswith(
        "models/example_domain/staging/base/example_domain_stg__model1/example_domain_stg__model1.yml"
    )
    assert domain_resource_location.get_model_metadata_filename("model1", ModelType.BASE, False) == "example_domain_stg__model1.yml"

    assert domain_resource_location.get_model_metadata_filename("model1", ModelType.STAGING, True).endswith(
        "models/example_domain/staging/marts_compatible/example_domain_stg__model1/example_domain_stg__model1.yml"
    )
    assert domain_resource_location.get_model_metadata_filename("model1", ModelType.STAGING, False) == "example_domain_stg__model1.yml"

    assert domain_resource_location.get_model_metadata_filename("model1", ModelType.MARTS, True).endswith(
        "models/example_domain/marts/example_domain__model1/example_domain__model1.yml"
    )
    assert domain_resource_location.get_model_metadata_filename("model1", ModelType.MARTS, False) == "example_domain__model1.yml"
