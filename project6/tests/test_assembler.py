from project6.code import code
from project6.parser import parse


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


def test_c_instruction_without_jump():
    result = parse("D=A")
    assert result.dest == "D"
    assert result.comp == "A"
    assert result.jump is None


def test_parse_ignores_whitespace():
    result = parse("  @42  ")
    assert result.number == 42


def test_parse_empty_line_returns_none():
    assert parse("") is None


def test_parse_whitespace_only_returns_none():
    assert parse("   ") is None


def test_parse_comment_line_returns_none():
    assert parse("// this is a comment") is None


def test_parse_inline_comment_is_stripped():
    result = parse("@42 // load 42")
    assert result.number == 42


def test_code_a_instruction():
    instruction = parse("@42")
    assert code(instruction) == "0000000000101010"


def test_code_c_instruction():
    instruction = parse("D=D+A;JGT")
    assert code(instruction) == "1110000010010001"