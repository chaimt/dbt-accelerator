import tempfile

from dbt_accelerator.companion.utils import FileHelper

temp_dir = tempfile.TemporaryDirectory().name


def test_touch():
    temp_file = f"{temp_dir}/missing.txt"
    try:
        assert not FileHelper.file_exists(temp_file)
        FileHelper.touch(temp_file)
    finally:
        FileHelper.delete_file(temp_file)
