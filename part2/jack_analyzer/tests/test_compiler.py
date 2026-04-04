from pathlib import Path
import pytest
from jack_analyzer.compiler import JackCompiler


TEST_DIR=Path("tests/test_data/Compiler")


@pytest.mark.parametrize("dir_name", ["Seven","ConvertToBin","Square","Average"])
def test_dirs_analyzed_as_expected(dir_name, tmp_path):
    current_dir = TEST_DIR / dir_name
    expected_dir = current_dir / "expected"
    compiler = JackCompiler(current_dir)
    compiler.compile(output_dir=tmp_path)
    jack_files = list(current_dir.glob("*.jack"))
    assert jack_files, f"No .jack files found in {current_dir}"
    for jack_file in jack_files:
        vm_name = jack_file.with_suffix(".vm").name
        expected_file = expected_dir / vm_name
        actual_file = tmp_path / vm_name
        assert expected_file.exists(), f"Missing expected file: {expected_file}"
        assert actual_file.read_text() == expected_file.read_text()
 