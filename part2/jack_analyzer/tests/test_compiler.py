from pathlib import Path
import pytest
from jack_analyzer.compiler import JackCompiler


TEST_DIR=Path("tests/test_data/Compiler")


@pytest.mark.parametrize("dir_name", ["Seven"])
def test_dirs_analyzed_as_expected(dir_name, tmp_path):
    current_dir = TEST_DIR / dir_name
    compiler = JackCompiler(current_dir)
    compiler.compile(output_dir=tmp_path)
    for expected_file in (current_dir / "expected").glob("*.vm"):
        actual_file = tmp_path / expected_file.name
        assert actual_file.read_text() == expected_file.read_text()
 