from dataclasses import dataclass


@dataclass
class AInstruction:
    number: int


@dataclass
class CInstruction:
    dest: str
    comp: str
    jump: str


def parse(line: str) -> AInstruction | CInstruction:
    if line.startswith("@"):
        return AInstruction(number=int(line[1:]))
    dest, rest = line.split("=")
    comp, jump = rest.split(";")
    return CInstruction(dest=dest, comp=comp, jump=jump)


def main() -> None:
    print("Hello from project6!")
