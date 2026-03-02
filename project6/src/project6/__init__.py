from dataclasses import dataclass


@dataclass
class AInstruction:
    number: int


@dataclass
class CInstruction:
    dest: str | None
    comp: str
    jump: str


def parse(line: str) -> AInstruction | CInstruction:
    if line.startswith("@"):
        return AInstruction(number=int(line[1:]))
    if "=" in line:
        dest, rest = line.split("=")
    else:
        dest = None
        rest = line
    comp, jump = rest.split(";")
    return CInstruction(dest=dest, comp=comp, jump=jump)


def main() -> None:
    print("Hello from project6!")
