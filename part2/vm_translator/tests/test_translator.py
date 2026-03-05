import shutil
from pathlib import Path
from vm_translator.translate import translate, translate_line


def test_push_constant_i():
    assert translate_line("push constant 7",1)=="""//(1) push constant 7
@7
D=A
@SP
A=M
M=D
@SP
M=M+1"""


def test_add():
    assert translate_line("add",1)=="""//(1) add
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

def test_eq():
    assert translate_line("eq",1)=="""//(1) eq
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=D-M
@EQ_CASE_1
D;JEQ
D=0
@END_1
0;JMP
(EQ_CASE_1)
D=-1
(END_1)
@SP
A=M
M=D
@SP
M=M+1"""

def test_lt():
    assert translate_line("lt",1)=="""//(1) lt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=D-M
@LT_CASE_1
D;JLT
D=0
@END_1
0;JMP
(LT_CASE_1)
D=-1
(END_1)
@SP
A=M
M=D
@SP
M=M+1"""

def test_gt():
    assert translate_line("gt",1)=="""//(1) gt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=D-M
@GT_CASE_1
D;JGT
D=0
@END_1
0;JMP
(GT_CASE_1)
D=-1
(END_1)
@SP
A=M
M=D
@SP
M=M+1"""



def test_translate_empty_line_returns_none():
    assert translate_line("",1) is None

def test_translate_comment_line_returns_none():
    assert translate_line("// this is a comment",1) is None


def test_translate_inline_comment_is_stripped():
    result = translate_line("push constant 7 // a comment",1)
    assert result == """//(1) push constant 7
@7
D=A
@SP
A=M
M=D
@SP
M=M+1"""

TEST_DATA = Path(__file__).parent / "test_data"

def test_simple_add_vm_file(tmp_path):
    name="SimpleAdd"
    shutil.copy(TEST_DATA / f"{name}.vm", tmp_path / f"{name}.vm")
    translate(tmp_path / f"{name}.vm")
    result = (tmp_path / f"{name}.asm").read_text()
    expected = (TEST_DATA / f"expected_{name}.asm").read_text()
    assert result == expected