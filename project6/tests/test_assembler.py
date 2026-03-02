from project6 import parse


def test_a_instruction_stores_number():
    result = parse("@42")
    assert result.number == 42