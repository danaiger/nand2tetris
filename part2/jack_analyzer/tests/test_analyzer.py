from jack_analyzer.analyzer import JackAnalyzer

def test_analyzer_writes_only_token_for_empty_file(tmp_path):
    file = tmp_path /"EmptyFile.jack"
    analyzer=JackAnalyzer(file)
    analyzer.tokenize()
    written_xml_file_path=tmp_path /"EmptyFileT.xml"
    xml_written=written_xml_file_path.read_text()
    assert xml_written=="""<tokens>
</tokens>"""
