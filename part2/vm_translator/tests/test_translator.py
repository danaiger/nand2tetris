import shutil
from pathlib import Path
import pytest
from vm_translator.translate import VMTranslator, translate_line


def test_push_constant_i():
    assert translate_line("push constant 7",1,"Test")=="""//(1) push constant 7
@7
D=A
@SP
A=M
M=D
@SP
M=M+1"""


def test_add():
    assert translate_line("add",1,"Test")=="""//(1) add
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
    assert translate_line("and",1,"Test")=="""//(1) and
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
    assert translate_line("or",1,"Test")=="""//(1) or
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
    assert translate_line("not",1,"Test")=="""//(1) not
@SP
M=M-1
A=M
M=!M
@SP
M=M+1"""

def test_sub():
    assert translate_line("sub",1,"Test")=="""//(1) sub
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
    assert translate_line("neg",1,"Test")=="""//(1) neg
@SP
M=M-1
A=M
M=-M
@SP
M=M+1"""

def test_eq():
    assert translate_line("eq",1,"Test")=="""//(1) eq
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
    assert translate_line("lt",1,"Test")=="""//(1) lt
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
    assert translate_line("gt",1,"Test")=="""//(1) gt
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
    assert translate_line("push local 2", 1, "Test") == """//(1) push local 2
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
    assert translate_line("push argument 2", 1, "Test") == """//(1) push argument 2
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
    assert translate_line("push this 2", 1, "Test") == """//(1) push this 2
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
    assert translate_line("push that 2", 1, "Test") == """//(1) push that 2
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
    assert translate_line("push temp 2", 1, "Test") == """//(1) push temp 2
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
    assert translate_line("pop local 2", 1, "Test") == """//(1) pop local 2
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
    assert translate_line("pop argument 2", 1, "Test") == """//(1) pop argument 2
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
    assert translate_line("pop this 2", 1, "Test") == """//(1) pop this 2
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
    assert translate_line("pop that 2", 1, "Test") == """//(1) pop that 2
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
    assert translate_line("pop temp 2", 1, "Test") == """//(1) pop temp 2
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


def test_push_pointer_0():
    assert translate_line("push pointer 0", 1, "Test") == """//(1) push pointer 0
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1"""


def test_push_pointer_1():
    assert translate_line("push pointer 1", 1, "Test") == """//(1) push pointer 1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1"""


def test_pop_pointer_0():
    assert translate_line("pop pointer 0", 1, "Test") == """//(1) pop pointer 0
@SP
M=M-1
A=M
D=M
@THIS
M=D"""


def test_pop_pointer_1():
    assert translate_line("pop pointer 1", 1, "Test") == """//(1) pop pointer 1
@SP
M=M-1
A=M
D=M
@THAT
M=D"""


def test_push_static():
    assert translate_line("push static 3", 1, "StaticTest") == """//(1) push static 3
@StaticTest.3
D=M
@SP
A=M
M=D
@SP
M=M+1"""


def test_pop_static():
    assert translate_line("pop static 8", 1, "StaticTest") == """//(1) pop static 8
@SP
M=M-1
A=M
D=M
@StaticTest.8
M=D"""


def test_label():
    assert translate_line("label LOOP", 1, "Test") == """//(1) label LOOP
(LOOP)"""


def test_if_goto():
    assert translate_line("if-goto LOOP", 1, "Test") == """//(1) if-goto LOOP
@SP
M=M-1
A=M
D=M
@LOOP
D;JNE"""


def test_goto():
    assert translate_line("goto LOOP", 1, "Test") == """//(1) goto LOOP
@LOOP
0;JMP"""


def test_translate_empty_line_returns_none():
    assert translate_line("",1,"Test") is None

def test_translate_comment_line_returns_none():
    assert translate_line("// this is a comment",1,"Test") is None


def test_translate_inline_comment_is_stripped():
    result = translate_line("push constant 7 // a comment",1,"Test")
    assert result == """//(1) push constant 7
@7
D=A
@SP
A=M
M=D
@SP
M=M+1"""

TEST_DATA = Path(__file__).parent / "test_data"

@pytest.mark.parametrize("name", ["SimpleAdd", "StackTest","BasicTest","PointerTest","StaticTest","BasicLoop","FibonacciSeries","SimpleFunction"])
def test_single_vm_file(tmp_path,name):
    shutil.copy(TEST_DATA / f"{name}.vm", tmp_path / f"{name}.vm")
    VMTranslator(tmp_path / f"{name}.vm")
    result = (tmp_path / f"{name}.asm").read_text()
    expected = (TEST_DATA / f"expected_{name}.asm").read_text()
    assert result == expected

@pytest.mark.parametrize("name", ["nested_call","fibonacci_element"])
def test_dir(tmp_path,name):
    shutil.copytree(TEST_DATA / f"{name}", tmp_path / f"{name}")
    VMTranslator(tmp_path / f"{name}")
    result = (tmp_path /f"{name}"/ f"{name}.asm").read_text()
    expected = (TEST_DATA /f"{name}"/ f"expected_{name}.asm").read_text()
    assert result == expected   