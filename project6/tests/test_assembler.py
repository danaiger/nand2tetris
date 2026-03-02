from project6 import parse


def test_a_instruction_stores_number():
    result = parse("@42")
    assert result.number == 42


def test_c_instruction_stores_dest_comp_jump():
    result = parse("D=A;JMP")
    assert result.dest == "D"
    assert result.comp == "A"
    assert result.jump == "JMP"


def test_c_instruction_without_dest():
    result = parse("0;JMP")
    assert result.dest is None
    assert result.comp == "0"
    assert result.jump == "JMP"