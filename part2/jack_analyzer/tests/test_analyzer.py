from pathlib import Path
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

def test_somethin():
    file = Path("tests/test_data/ArrayTest/Main.Jack") 
    analyzer=JackAnalyzer(file)
    analyzer.tokenize()
    written_xml_file_path= Path("tests/test_data/ArrayTest/MainT.xml")
    expected_written_xml_file_path= Path("tests/test_data/ArrayTest/expected_MainT.xml")
    xml_written=written_xml_file_path.read_text()
    expected_xml=expected_written_xml_file_path.read_text()
    assert xml_written==expected_xml