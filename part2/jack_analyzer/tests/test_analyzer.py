from jack_analyzer.analyzer import JackAnalyzer
from jack_analyzer.tokenizer import JackTokenizer

def test_placeholder():
    assert True

def test_analyzer_writes_only_token_for_empty_file(tmp_path):
    file = tmp_path /"EmptyFile.jack"
    analyzer=JackAnalyzer(file)
    analyzer.tokenize()
    written_xml_file_path=tmp_path /"EmptyFileT.xml"
    xml_written=written_xml_file_path.read_text()
    assert xml_written=="""<tokens>
</tokens>"""

def test_has_more_tokens_is_false_on_spaces_and_newlines(tmp_path):
    file = tmp_path /"EmptyFile.jack"
    file.write_text("        \n  \n ")
    with open(file) as f:
        tokenizer=JackTokenizer(f)
        assert tokenizer.has_more_tokens()==False

def test_has_more_tokens_is_true_for_class(tmp_path):
    file = tmp_path /"EmptyFile.jack"
    file.write_text("class")
    with open(file) as f:
        tokenizer=JackTokenizer(f)
        assert tokenizer.has_more_tokens()==True

def test_has_more_tokens_is_false_for_inline_comment(tmp_path):
    file = tmp_path /"EmptyFile.jack"
    file.write_text(" \n   // an inline comment ")
    with open(file) as f:
        tokenizer=JackTokenizer(f)
        assert tokenizer.has_more_tokens()==False

def test_current_token_updated_to_class_after_advancing(tmp_path):
    file = tmp_path /"EmptyFile.jack"
    file.write_text("class")
    with open(file) as f:
        tokenizer=JackTokenizer(f)
        tokenizer.advance()
        assert tokenizer.get_current_token()=="class"

def test_has_more_tokens_before_adavancing_and_has_not_after(tmp_path):
    file = tmp_path /"EmptyFile.jack"
    file.write_text("class")
    with open(file) as f:
        tokenizer=JackTokenizer(f)
        assert tokenizer.has_more_tokens()==True
        tokenizer.advance()
        assert tokenizer.get_current_token()=="class"
        assert tokenizer.has_more_tokens()==False

def test_can_infer_class_token_while_ignoring_preceding_newlines_spaces_and_inline_comments(tmp_path):
    file = tmp_path /"EmptyFile.jack"
    file.write_text("""    //some_comment
    //more comments
                    class""")
    with open(file) as f:
        tokenizer=JackTokenizer(f)
        assert tokenizer.has_more_tokens()==True
        tokenizer.advance()
        assert tokenizer.get_current_token()=="class"
        assert tokenizer.has_more_tokens()==False

def test_can_infer_class_token_while_ignoring_trailing_newlines_spaces_and_inline_comments(tmp_path):
    file = tmp_path /"EmptyFile.jack"
    file.write_text("""class //a comment
           //another comment
                             """)
    with open(file) as f:
        tokenizer=JackTokenizer(f)
        assert tokenizer.has_more_tokens()==True
        tokenizer.advance()
        assert tokenizer.get_current_token()=="class"
        assert tokenizer.has_more_tokens()==False
