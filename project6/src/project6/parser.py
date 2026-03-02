from dataclasses import dataclass


@dataclass
class AInstruction:
    number: int


@dataclass
class CInstruction:
    dest: str | None
    comp: str
    jump: str | None


@dataclass
class LabelInstruction:
    label: str


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


def parse(line: str) -> AInstruction | CInstruction | LabelInstruction | None:
    line = line.split("//")[0].strip()
    if not line:
        return None
    if line.startswith("@"):
        return parse_a_instruction(line)
    if line.startswith("("):
        return LabelInstruction(label=line[1:-1])
    return parse_c_instruction(line)
