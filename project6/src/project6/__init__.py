from dataclasses import dataclass


@dataclass
class AInstruction:
    number: int


def parse(line: str) -> AInstruction:
    return AInstruction(number=int(line[1:]))


def main() -> None:
    print("Hello from project6!")
