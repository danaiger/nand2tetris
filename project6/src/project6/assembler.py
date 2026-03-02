from pathlib import Path


def assemble(path: Path) -> None:
    with open(path) as asm, open(path.with_suffix(".hack"), "w") as hack:
        for line in asm:
            pass
