# pylint: disable=missing-module-docstring,missing-function-docstring
from pathlib import Path
import pytest
from snakeglish.description import code_to_description


@pytest.mark.parametrize('case_dir', list(Path('test_cases').iterdir()))
def test_code_to_description(case_dir, snapshot):
    # Read input files from the case directory.
    python_code = case_dir.joinpath('code.py').read_text()

    # Call the tested function.
    code_description = code_to_description(python_code)

    # Snapshot the return value.
    snapshot.snapshot_dir = case_dir
    snapshot.assert_match(code_description, 'description.txt')
