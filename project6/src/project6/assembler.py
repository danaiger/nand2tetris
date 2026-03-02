from pathlib import Path

from project6.code import code
from project6.parser import AInstruction, parse, LabelInstruction

PREDEFINED_SYMBOLS = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576,
    **{f"R{i}": i for i in range(16)},
}


def _build_symbol_table(path: Path) -> dict[str, int]:
    symbol_table = dict(PREDEFINED_SYMBOLS)
    with open(path) as asm:
        instruction_count = 0
        for line in asm:
            instruction = parse(line)
            if isinstance(instruction, LabelInstruction):
                symbol_table[instruction.label] = instruction_count
            elif instruction is not None:
                instruction_count += 1
    return symbol_table


def _resolve_symbol(
    symbol: str, symbol_table: dict[str, int], next_available_register: int
) -> tuple[int, int]:
    if symbol not in symbol_table:
        symbol_table[symbol] = next_available_register
        next_available_register += 1
    return symbol_table[symbol], next_available_register


def _emit(path: Path, symbol_table: dict[str, int]) -> None:
    next_available_register = 16
    with open(path) as asm, open(path.with_suffix(".hack"), "w") as hack:
        first = True
        for line in asm:
            instruction = parse(line)
            if instruction is not None and not isinstance(
                instruction, LabelInstruction
            ):
                if isinstance(instruction, AInstruction) and isinstance(
                    instruction.value, str
                ):
                    address, next_available_register = _resolve_symbol(
                        instruction.value, symbol_table, next_available_register
                    )
                    instruction = AInstruction(value=address)
                if not first:
                    hack.write("\n")
                hack.write(code(instruction))
                first = False


def assemble(path: Path) -> None:
    symbol_table = _build_symbol_table(path)
    _emit(path, symbol_table)
