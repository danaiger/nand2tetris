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
