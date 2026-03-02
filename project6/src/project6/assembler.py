from pathlib import Path

from project6.code import code
from project6.parser import AInstruction, parse

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


def assemble(path: Path) -> None:
    symbol_table = dict(PREDEFINED_SYMBOLS)
    with open(path) as asm, open(path.with_suffix(".hack"), "w") as hack:
        first = True
        for line in asm:
            instruction = parse(line)
            if instruction is not None:
                if isinstance(instruction, AInstruction) and isinstance(instruction.value, str):
                    instruction = AInstruction(value=symbol_table[instruction.value])
                if not first:
                    hack.write("\n")
                hack.write(code(instruction))
                first = False
