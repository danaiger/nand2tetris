from pathlib import Path
import sys

SEGMENT_TO_SHORTCUT={
    "local":"LCL",
    "argument":"ARG",
    "this":"THIS",
    "that":"THAT",
}

NUMBER_TO_POINTER={
    "0":"THIS",
    "1":"THAT"
}

def translate_line(line:str,line_number:int,filename:str)->str | None:
    line = line.split("//")[0].strip()
    if not line:
        return None
    comment=f'//({line_number}) {line}'
    splitted=line.split(' ')
    command=splitted[0]
    print(command)
    if command=="push":
        segment=splitted[1]
        number=splitted[2]
        if segment=="constant":
            generated_code=f'''
@{number}
D=A
@SP
A=M
M=D
@SP
M=M+1'''
        elif segment in SEGMENT_TO_SHORTCUT.keys():
            generated_code=f'''
@{SEGMENT_TO_SHORTCUT[segment]}
D=M
@{number}
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1'''
        elif segment == "temp":
            generated_code=f'''
@5
D=A
@{number}
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1'''
        elif segment=="pointer":
            generated_code=f'''
@{NUMBER_TO_POINTER[number]}
D=M
@SP
A=M
M=D
@SP
M=M+1'''
        elif segment=="static":
            generated_code=f'''
@{filename}.{number}
D=M
@SP
A=M
M=D
@SP
M=M+1'''
    elif command=="pop":
        segment=splitted[1]
        number=splitted[2]
        if segment in SEGMENT_TO_SHORTCUT.keys():
             generated_code=f'''
@{SEGMENT_TO_SHORTCUT[segment]}
D=M
@{number}
D=D+A
@SP
A=M
M=D
A=A-1
D=M
A=A+1
A=M
M=D
@SP
M=M-1'''           

        elif segment =="temp":
             generated_code=f'''
@5
D=A
@{number}
D=D+A
@SP
A=M
M=D
A=A-1
D=M
A=A+1
A=M
M=D
@SP
M=M-1'''

        elif segment=="pointer":
            generated_code=f'''
@SP
M=M-1
A=M
D=M
@{NUMBER_TO_POINTER[number]}
M=D'''

        elif segment=="static":
            generated_code=f'''
@SP
M=M-1
A=M
D=M
@{filename}.{number}
M=D'''

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

    elif command =="and":
        generated_code=f'''
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=D&M
M=D
@SP
M=M+1'''

    elif command =="or":
        generated_code=f'''
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=D|M
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

    elif command =="neg":
        generated_code=f'''
@SP
M=M-1
A=M
M=-M
@SP
M=M+1'''

    elif command =="not":
        generated_code=f'''
@SP
M=M-1
A=M
M=!M
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

    elif command=="label":
        name=splitted[1]
        generated_code=f'''
({name})'''

    elif command=="if-goto":
        dest=splitted[1]
        generated_code=f'''
@SP
M=M-1
A=M
D=M
@{dest}
D;JGT'''

    elif command=="goto":
        dest=splitted[1]
        generated_code=f'''
@{dest}
0;JMP'''

    return comment+generated_code


def translate(path: Path):
    line_number=0
    with open(path) as vm, open(path.with_suffix(".asm"), "w") as asm:
        for line in vm:
            translated=translate_line(line,line_number,path.stem)
            if translated is not None:
                asm.write(f"{translated}\n")
                line_number+=1

def main():
    translate(Path(sys.argv[1]))

if __name__ == '__main__':
    main()