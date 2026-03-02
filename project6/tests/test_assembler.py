import shutil
from pathlib import Path

import pytest

from project6.assembler import assemble
from project6.code import code
from project6.parser import parse


def test_assemble_empty_file(tmp_path):
    asm_file = tmp_path / "empty.asm"
    asm_file.write_text("")
    assemble(asm_file)
    hack_file = tmp_path / "empty.hack"
    assert hack_file.read_text() == ""


def test_a_instruction_with_number_stores_int():
    result = parse("@42")
    assert result.value == 42


def test_a_instruction_with_symbol_stores_str():
    result = parse("@R0")
    assert result.value == "R0"


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
    assert result.value == 42


def test_parse_empty_line_returns_none():
    assert parse("") is None


def test_parse_whitespace_only_returns_none():
    assert parse("   ") is None


def test_parse_comment_line_returns_none():
    assert parse("// this is a comment") is None


def test_parse_inline_comment_is_stripped():
    result = parse("@42 // load 42")
    assert result.value == 42


def test_parse_label_instruction():
    result = parse("(LOOP)")
    assert result.label == "LOOP"


def test_code_a_instruction():
    instruction = parse("@42")
    assert code(instruction) == "0000000000101010"


def test_code_c_instruction():
    instruction = parse("D=D+A;JGT")
    assert code(instruction) == "1110000010010001"


TEST_DATA = Path(__file__).parent / "test_data"


def test_assemble_add(tmp_path):
    shutil.copy(TEST_DATA / "Add.asm", tmp_path / "Add.asm")
    assemble(tmp_path / "Add.asm")
    result = (tmp_path / "Add.hack").read_text()
    expected = (TEST_DATA / "expected_Add.hack").read_text()
    assert result == expected


@pytest.mark.parametrize("name", ["Max", "Rect", "Pong"])
def test_assemble_symbolless(tmp_path, name):
    shutil.copy(TEST_DATA / f"{name}L.asm", tmp_path / f"{name}L.asm")
    assemble(tmp_path / f"{name}L.asm")
    result = (tmp_path / f"{name}L.hack").read_text()
    expected = (TEST_DATA / f"expected_{name}.hack").read_text()
    assert result == expected


def test_assemble_predefined_symbol(tmp_path):
    asm_file = tmp_path / "predefined.asm"
    asm_file.write_text("@R0\n")
    assemble(asm_file)
    result = (tmp_path / "predefined.hack").read_text()
    assert result == "0000000000000000"


def test_assemble_label_symbol(tmp_path):
    asm_file = tmp_path / "label.asm"
    asm_file.write_text("(LOOP)\n@LOOP\n0;JMP\n")
    assemble(asm_file)
    result = (tmp_path / "label.hack").read_text()
    assert result == "0000000000000000\n1110101010000111"
