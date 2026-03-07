import shutil
from pathlib import Path
import pytest
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

def test_and():
    assert translate_line("and",1)=="""//(1) and
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=D&M
M=D
@SP
M=M+1"""

def test_or():
    assert translate_line("or",1)=="""//(1) or
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=D|M
M=D
@SP
M=M+1"""

def test_not():
    assert translate_line("not",1)=="""//(1) not
@SP
M=M-1
A=M
M=!M
@SP
M=M+1"""

def test_sub():
    assert translate_line("sub",1)=="""//(1) sub
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
M=D
@SP
M=M+1"""


def test_neg():
    assert translate_line("neg",1)=="""//(1) neg
@SP
M=M-1
A=M
M=-M
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
D=M-D
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
D=M-D
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
D=M-D
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



def test_push_local():
    assert translate_line("push local 2", 1) == """//(1) push local 2
@LCL
D=M
@2
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1"""


def test_push_argument():
    assert translate_line("push argument 2", 1) == """//(1) push argument 2
@ARG
D=M
@2
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1"""


def test_push_this():
    assert translate_line("push this 2", 1) == """//(1) push this 2
@THIS
D=M
@2
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1"""


def test_push_that():
    assert translate_line("push that 2", 1) == """//(1) push that 2
@THAT
D=M
@2
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1"""


def test_push_temp():
    assert translate_line("push temp 2", 1) == """//(1) push temp 2
@5
D=A
@2
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1"""


def test_pop_local():
    assert translate_line("pop local 2", 1) == """//(1) pop local 2
@LCL
D=M
@2
D=D+A
@SP
A=M
M=D
A=A-1
D=M
A=A+1
A=M
M=D
@SP
M=M-1"""


def test_pop_argument():
    assert translate_line("pop argument 2", 1) == """//(1) pop argument 2
@ARG
D=M
@2
D=D+A
@SP
A=M
M=D
A=A-1
D=M
A=A+1
A=M
M=D
@SP
M=M-1"""


def test_pop_this():
    assert translate_line("pop this 2", 1) == """//(1) pop this 2
@THIS
D=M
@2
D=D+A
@SP
A=M
M=D
A=A-1
D=M
A=A+1
A=M
M=D
@SP
M=M-1"""


def test_pop_that():
    assert translate_line("pop that 2", 1) == """//(1) pop that 2
@THAT
D=M
@2
D=D+A
@SP
A=M
M=D
A=A-1
D=M
A=A+1
A=M
M=D
@SP
M=M-1"""


def test_pop_temp():
    assert translate_line("pop temp 2", 1) == """//(1) pop temp 2
@5
D=A
@2
D=D+A
@SP
A=M
M=D
A=A-1
D=M
A=A+1
A=M
M=D
@SP
M=M-1"""


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

@pytest.mark.parametrize("name", ["SimpleAdd", "StackTest","BasicTest"])
def test_simple_add_vm_file(tmp_path,name):
    shutil.copy(TEST_DATA / f"{name}.vm", tmp_path / f"{name}.vm")
    translate(tmp_path / f"{name}.vm")
    result = (tmp_path / f"{name}.asm").read_text()
    expected = (TEST_DATA / f"expected_{name}.asm").read_text()
    assert result == expected