from dataclasses import dataclass


@dataclass
class AInstruction:
    number: int


@dataclass
class CInstruction:
    dest: str | None
    comp: str
    jump: str | None


def parse_a_instruction(line: str) -> AInstruction:
    return AInstruction(number=int(line[1:]))


def parse_c_instruction(line: str) -> CInstruction:
    if "=" in line:
        dest, rest = line.split("=")
    else:
        dest = None
        rest = line
    if ";" in rest:
        comp, jump = rest.split(";")
    else:
        comp = rest
        jump = None
    return CInstruction(dest=dest, comp=comp, jump=jump)


def code(instruction: AInstruction | CInstruction) -> str:
    if isinstance(instruction, AInstruction):
        return f"{instruction.number:016b}"


def parse(line: str) -> AInstruction | CInstruction | None:
    line = line.split("//")[0].strip()
    if not line:
        return None
    if line.startswith("@"):
        return parse_a_instruction(line)
    return parse_c_instruction(line)


def main() -> None:
    print("Hello from project6!")
