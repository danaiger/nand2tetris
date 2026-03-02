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


def assemble(path: Path) -> None:
    symbol_table = dict(PREDEFINED_SYMBOLS)
    with open(path) as asm:
        instruction_count = 0
        for line in asm:
            instruction = parse(line)
            if isinstance(instruction, LabelInstruction):
                symbol_table[instruction.label] = instruction_count
            elif instruction is not None:
                instruction_count += 1

    FIRST_AVAILABLE_REGISTER=16
    next_available_register=FIRST_AVAILABLE_REGISTER
    with open(path) as asm, open(path.with_suffix(".hack"), "w") as hack:
        first = True
        for line in asm:
            instruction = parse(line)
            if instruction is not None and not isinstance(instruction, LabelInstruction):
                if isinstance(instruction, AInstruction) and isinstance(instruction.value, str):
                    if not instruction.value in symbol_table:
                        symbol_table[instruction.value]=next_available_register
                        next_available_register+=1
                    instruction = AInstruction(value=symbol_table[instruction.value])
                if not first:
                    hack.write("\n")
                hack.write(code(instruction))
                first = False
