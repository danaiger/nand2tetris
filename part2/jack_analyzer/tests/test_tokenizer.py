import pytest
from jack_analyzer.tokenizer import JACK_SYMBOLS, JackTokenizer, TokenType
from jack_analyzer.tokenizer import JACK_KEYWORDS

def test_has_more_tokens_is_false_on_spaces_and_newlines_and_tabs(tmp_path):
    file = tmp_path /"File.jack"
    file.write_text("     \t   \n  \n ")
    with open(file) as f:
        tokenizer=JackTokenizer(f)
        assert tokenizer.has_more_tokens()==False

def test_has_more_tokens_is_true_for_class(tmp_path):
    file = tmp_path /"File.jack"
    file.write_text("class")
    with open(file) as f:
        tokenizer=JackTokenizer(f)
        assert tokenizer.has_more_tokens()==True

def test_has_more_tokens_is_false_for_inline_comment(tmp_path):
    file = tmp_path /"File.jack"
    file.write_text(" \n   // an inline comment ")
    with open(file) as f:
        tokenizer=JackTokenizer(f)
        assert tokenizer.has_more_tokens()==False

def test_has_more_tokens_is_false_for_two_inline_comment(tmp_path):
    file = tmp_path /"File.jack"
    file.write_text("// an inline comment\n// another comment")
    with open(file) as f:
        tokenizer=JackTokenizer(f)
        assert tokenizer.has_more_tokens()==False

def test_has_more_tokens_is_false_for_two_mutiline_comments(tmp_path):
    file = tmp_path /"File.jack"
    file.write_text("/* an inline comment\n nanana*//* another comment\n lalala*/")
    with open(file) as f:
        tokenizer=JackTokenizer(f)
        assert tokenizer.has_more_tokens()==False

def test_has_more_tokens_is_false_for_multiline_comment(tmp_path):
    file = tmp_path /"File.jack"
    file.write_text(""" \n   /* a
                    multiline
                    comment
                    */""")
    with open(file) as f:
        tokenizer=JackTokenizer(f)
        assert tokenizer.has_more_tokens()==False

def test_current_token_updated_to_class_after_advancing(tmp_path):
    file = tmp_path /"File.jack"
    file.write_text("class")
    with open(file) as f:
        tokenizer=JackTokenizer(f)
        tokenizer.advance()
        assert tokenizer.get_current_token()=="class"

def test_has_more_tokens_before_adavancing_and_has_not_after(tmp_path):
    file = tmp_path /"File.jack"
    file.write_text("class")
    with open(file) as f:
        tokenizer=JackTokenizer(f)
        assert tokenizer.has_more_tokens()==True
        tokenizer.advance()
        assert tokenizer.get_current_token()=="class"
        assert tokenizer.has_more_tokens()==False

def test_can_infer_class_token_while_ignoring_preceding_newlines_spaces_and_inline_comments(tmp_path):
    file = tmp_path /"File.jack"
    file.write_text(""" \t   //some_comment 
    //more comments
             \t       class""")
    with open(file) as f:
        tokenizer=JackTokenizer(f)
        assert tokenizer.has_more_tokens()==True
        tokenizer.advance()
        assert tokenizer.get_current_token()=="class"
        assert tokenizer.has_more_tokens()==False

def test_can_infer_class_token_while_ignoring_trailing_newlines_spaces_and_inline_comments(tmp_path):
    file = tmp_path /"File.jack"
    file.write_text("""class \t //a comment
      \t  //another comment
                      \t       """)
    with open(file) as f:
        tokenizer=JackTokenizer(f)
        assert tokenizer.has_more_tokens()==True
        tokenizer.advance()
        assert tokenizer.get_current_token()=="class"
        assert tokenizer.has_more_tokens()==False

@pytest.mark.parametrize("name", JACK_KEYWORDS)
def test_token_type_is_keyword_for_keywords(tmp_path,name):
    file = tmp_path /"File.jack"
    file.write_text(f"""{name}""")
    with open(file) as f:
        tokenizer=JackTokenizer(f)
        assert tokenizer.has_more_tokens()==True
        tokenizer.advance()
        assert tokenizer.get_current_token()==f"{name}"
        assert tokenizer.token_type()==TokenType.keyword

@pytest.mark.parametrize("name", JACK_SYMBOLS)
def test_token_type_is_symbol_for_symbols(tmp_path,name):
    file = tmp_path /"File.jack"
    file.write_text(f"""{name}""")
    with open(file) as f:
        tokenizer=JackTokenizer(f)
        assert tokenizer.has_more_tokens()==True
        tokenizer.advance()
        assert tokenizer.get_current_token()==f"{name}"
        assert tokenizer.token_type()==TokenType.symbol

def test_token_type_is_string_const_for_somestring(tmp_path):
    file = tmp_path /"File.jack"
    file.write_text('''"somestring"''')
    with open(file) as f:
        tokenizer=JackTokenizer(f)
        assert tokenizer.has_more_tokens()==True
        tokenizer.advance()
        assert tokenizer.get_current_token()=='"somestring"'
        assert tokenizer.token_type()==TokenType.string_const

def test_token_type_is_int_const_for_arbitrary_number(tmp_path):
    file = tmp_path /"File.jack"
    file.write_text('''1235''')
    with open(file) as f:
        tokenizer=JackTokenizer(f)
        assert tokenizer.has_more_tokens()==True
        tokenizer.advance()
        assert tokenizer.get_current_token()=='1235'
        assert tokenizer.token_type()==TokenType.int_const

def test_number_then_symbol(tmp_path):
    file = tmp_path /"File.jack"
    file.write_text("13;")
    with open(file) as f:
        tokenizer=JackTokenizer(f)
        tokenizer.advance()
        assert tokenizer.get_current_token()=="13"
        tokenizer.advance()
        assert tokenizer.get_current_token()==";"

def test_string_token_adjacent_to_symbol_is_interpreted_as_two_tokens(tmp_path):
    file = tmp_path /"File.jack"
    file.write_text('''"somestring";''')
    with open(file) as f:
        tokenizer=JackTokenizer(f)
        assert tokenizer.has_more_tokens()==True
        tokenizer.advance()
        assert tokenizer.get_current_token()=='"somestring"'
        assert tokenizer.has_more_tokens()==True
        tokenizer.advance()
        assert tokenizer.has_more_tokens()==False
        assert tokenizer.get_current_token()==';'

def test_token_type_is_identifier_for_someidentifier(tmp_path):
    file = tmp_path /"File.jack"
    file.write_text('''someidentifier''')
    with open(file) as f:
        tokenizer=JackTokenizer(f)
        assert tokenizer.has_more_tokens()==True
        tokenizer.advance()
        assert tokenizer.get_current_token()=='someidentifier'
        assert tokenizer.token_type()==TokenType.identifier


def test_number_is_interpreted_as_digits_only(tmp_path):
    file = tmp_path /"File.jack"
    file.write_text('''2345;''')
    with open(file) as f:
        tokenizer=JackTokenizer(f)
        assert tokenizer.has_more_tokens()==True
        tokenizer.advance()
        assert tokenizer.get_current_token()=='2345'
        assert tokenizer.token_type()==TokenType.int_const

@pytest.mark.parametrize("symbol", JACK_SYMBOLS)
def test_symbol_is_tokenized_as_one_character(tmp_path,symbol):
    file = tmp_path /"File.jack"
    file.write_text(f'''{symbol}a''')
    with open(file) as f:
        tokenizer=JackTokenizer(f)
        assert tokenizer.has_more_tokens()==True
        tokenizer.advance()
        assert tokenizer.get_current_token()==symbol
        assert tokenizer.token_type()==TokenType.symbol

CHAR_OUTSIDE_IDENTIFIER=JACK_SYMBOLS.union({'',' ','\n','"'})
@pytest.mark.parametrize("char_outside_identifier", CHAR_OUTSIDE_IDENTIFIER)
def test_identifier_is_tokenized_properly(tmp_path,char_outside_identifier):
    file = tmp_path /"File.jack"
    file.write_text(f'''identifier{char_outside_identifier}''')
    with open(file) as f:
        tokenizer=JackTokenizer(f)
        assert tokenizer.has_more_tokens()==True
        tokenizer.advance()
        assert tokenizer.get_current_token()=="identifier"
        assert tokenizer.token_type()==TokenType.identifier

@pytest.mark.parametrize("symbol", JACK_SYMBOLS)
def test_identifier_then_symbol(tmp_path,symbol):
    file = tmp_path /"File.jack"
    file.write_text(f'''identifier{symbol}''')
    with open(file) as f:
        tokenizer=JackTokenizer(f)
        assert tokenizer.has_more_tokens()==True
        tokenizer.advance()
        assert tokenizer.get_current_token()=="identifier"
        assert tokenizer.token_type()==TokenType.identifier
        tokenizer.advance()
        assert tokenizer.get_current_token()==symbol
        assert tokenizer.token_type()==TokenType.symbol
        


def test_tab_after_inline_comment(tmp_path):
    file = tmp_path /"File.jack"
    file.write_text(""" sometext    // -6 for ball size
\t someothertext """)
    with open(file) as f:
        tokenizer=JackTokenizer(f)
        tokenizer.advance()
        assert tokenizer.get_current_token()=="sometext" 
        tokenizer.advance()
        assert tokenizer.get_current_token()=="someothertext" 