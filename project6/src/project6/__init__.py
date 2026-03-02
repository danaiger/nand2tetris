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


COMP_TABLE = {
    "0":   "0101010",
    "1":   "0111111",
    "-1":  "0111010",
    "D":   "0001100",
    "A":   "0110000",
    "!D":  "0001101",
    "!A":  "0110001",
    "-D":  "0001111",
    "-A":  "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M":   "1110000",
    "!M":  "1110001",
    "-M":  "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101",
}

DEST_TABLE = {
    None:  "000",
    "M":   "001",
    "D":   "010",
    "MD":  "011",
    "A":   "100",
    "AM":  "101",
    "AD":  "110",
    "AMD": "111",
}

JUMP_TABLE = {
    None:  "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111",
}


def code(instruction: AInstruction | CInstruction) -> str:
    if isinstance(instruction, AInstruction):
        return f"{instruction.number:016b}"
    return "111" + COMP_TABLE[instruction.comp] + DEST_TABLE[instruction.dest] + JUMP_TABLE[instruction.jump]


def parse(line: str) -> AInstruction | CInstruction | None:
    line = line.split("//")[0].strip()
    if not line:
        return None
    if line.startswith("@"):
        return parse_a_instruction(line)
    return parse_c_instruction(line)


def main() -> None:
    print("Hello from project6!")
