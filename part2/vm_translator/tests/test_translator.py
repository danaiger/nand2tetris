from vm_translator.translate import translate_line


def test_push_constant_i():
    assert translate_line("push constant 7")=="""// push constant 7
@7
D=A
@SP
A=M
M=D
@SP
M=M+1"""


def test_add():
    assert translate_line("add")=="""// add
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=D+M
M=D
@SP
M=M+1"""

def test_translate_empty_line_returns_none():
    assert translate_line("") is None

def test_translate_comment_line_returns_none():
    assert translate_line("// this is a comment") is None


def test_translate_inline_comment_is_stripped():
    result = translate_line("push constant 7 // a comment")
    assert result == """// push constant 7
@7
D=A
@SP
A=M
M=D
@SP
M=M+1"""