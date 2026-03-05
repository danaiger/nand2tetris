from pathlib import Path
import sys

def translate_line(line:str,line_number:int)->str | None:
    line = line.split("//")[0].strip()
    # generated_code=""
    if not line:
        return None
    comment=f'//({line_number}) {line}'
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

    elif command =="sub":
        generated_code=f'''
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
M=D
@SP
M=M+1'''

    elif command=="eq" or command =="lt" or command=="gt":
        generated_code=f'''
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@{command.upper()}_CASE_{line_number}
D;J{command.upper()}
D=0
@END_{line_number}
0;JMP
({command.upper()}_CASE_{line_number})
D=-1
(END_{line_number})
@SP
A=M
M=D
@SP
M=M+1'''
    return comment+generated_code


def translate(path: Path):
    line_number=0
    with open(path) as vm, open(path.with_suffix(".asm"), "w") as asm:
        for line in vm:
            translated=translate_line(line,line_number)
            if translated is not None:
                asm.write(f"{translated}\n")
                line_number+=1

def main():
    translate(Path(sys.argv[1]))

if __name__ == '__main__':
    main()