from pathlib import Path

from project6.code import code
from project6.parser import parse


def assemble(path: Path) -> None:
    with open(path) as asm, open(path.with_suffix(".hack"), "w") as hack:
        first = True
        for line in asm:
            instruction = parse(line)
            if instruction is not None:
                if not first:
                    hack.write("\n")
                hack.write(code(instruction))
                first = False
