from pathlib import Path
import sys

def translate_line(line:str)->str | None:
    line = line.split("//")[0].strip()
    # generated_code=""
    if not line:
        return None
    comment=f'// {line}'
    splitted=line.split(' ')
    command=splitted[0]
    if command=="push":
        number=splitted[2]
        generated_code=f'''
@{number}
D=A
@SP
A=M
M=D
@SP
M=M+1'''
    elif command =="add":
        generated_code=f'''
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=D+M
M=D
@SP
M=M+1'''

    elif command=="eq" or command =="lt":
        generated_code=f'''
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=D-M
@{command.upper()}_CASE
D;J{command.upper()}
D=0
@END
0;JMP
({command.upper()}_CASE)
D=-1
(END)
@SP
A=M
M=D
@SP
M=M+1'''

    return comment+generated_code


def translate(path: Path):
    with open(path) as vm, open(path.with_suffix(".asm"), "w") as asm:
        for line in vm:
            translated=translate_line(line)
            if translated is not None:
                asm.write(f"{translated}\n")

def main():
    translate(Path(sys.argv[1]))

if __name__ == '__main__':
    main()