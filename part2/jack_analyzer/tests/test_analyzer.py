from pathlib import Path
import pytest
from jack_analyzer.analyzer import JackAnalyzer

def test_analyzer_writes_only_token_for_empty_file(tmp_path):
    file = tmp_path /"EmptyFile.jack"
    file.write_text("")
    analyzer=JackAnalyzer(file)
    analyzer.tokenize()
    written_xml_file_path=tmp_path /"EmptyFileT.xml"
    xml_written=written_xml_file_path.read_text()
    assert xml_written=="""<tokens>
</tokens>
"""

TEST_DIR=Path("tests/test_data")
@pytest.mark.parametrize("dir_name", ["ArrayTest","ExpressionLessSquare","Square"])
def test_dirs_tokenize_as_expected(dir_name):
    current_dir=TEST_DIR/dir_name
    analyzer=JackAnalyzer(current_dir)
    analyzer.tokenize()
    for expected_file in current_dir.glob("expected_*T.xml"):
        actual_file = expected_file.with_name(expected_file.name.removeprefix("expected_"))
        assert actual_file.read_text() == expected_file.read_text()