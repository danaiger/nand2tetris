from io import TextIOWrapper
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

POP_TO_D='''\
@SP
M=M-1
A=M
D=M'''

PUSH_D='''\
@SP
A=M
M=D
@SP
M=M+1'''

def _scoped_label(name, current_function=None):
    if current_function:
        return f"{current_function}${name}"
    return name

def translate_line(line:str,line_number:int,filename:str,current_function:str|None=None)->str | None:
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
{PUSH_D}'''
        elif segment in SEGMENT_TO_SHORTCUT.keys():
            generated_code=f'''
@{SEGMENT_TO_SHORTCUT[segment]}
D=M
@{number}
A=D+A
D=M
{PUSH_D}'''
        elif segment == "temp":
            generated_code=f'''
@5
D=A
@{number}
A=D+A
D=M
{PUSH_D}'''
        elif segment=="pointer":
            generated_code=f'''
@{NUMBER_TO_POINTER[number]}
D=M
{PUSH_D}'''
        elif segment=="static":
            generated_code=f'''
@{filename}.{number}
D=M
{PUSH_D}'''
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
{POP_TO_D}
@SP
M=M-1
A=M
D=D+M
M=D
@SP
M=M+1'''

    elif command =="and":
        generated_code=f'''
{POP_TO_D}
@SP
M=M-1
A=M
D=D&M
M=D
@SP
M=M+1'''

    elif command =="or":
        generated_code=f'''
{POP_TO_D}
@SP
M=M-1
A=M
D=D|M
M=D
@SP
M=M+1'''

    elif command =="sub":
        generated_code=f'''
{POP_TO_D}
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
{POP_TO_D}
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
{PUSH_D}'''

    elif command=="label":
        name=splitted[1]
        generated_code=f'''
({_scoped_label(name,current_function)})'''

    elif command=="if-goto":
        dest=splitted[1]
        generated_code=f'''
{POP_TO_D}
@{_scoped_label(dest,current_function)}
D;JNE'''

    elif command=="goto":
        dest=splitted[1]
        generated_code=f'''
@{_scoped_label(dest,current_function)}
0;JMP'''

    elif command=="function":
        name=splitted[1]
        nvars=splitted[2]
        generated_code=f'''
({name})
@{nvars}
D=A
@FINISH_{line_number}
D;JEQ
@n
M=D
@i
M=0
(LOOP_{line_number})
@0
D=A
{PUSH_D}
@i
DM=M+1
@n
D=D-M
@LOOP_{line_number}
D;JLT
(FINISH_{line_number})
'''

    elif command=="return":
        generated_code=f'''
@LCL
D=M
@endFrame
M=D
@5
D=D-A
A=D
D=M
@retAddr
M=D
{POP_TO_D}
@ARG
A=M
M=D
@ARG
D=M
@SP
M=D+1
@endFrame
A=M-1
D=M
@THAT
M=D
@endFrame
A=M-1
A=A-1
D=M
@THIS
M=D
@endFrame
A=M-1
A=A-1
A=A-1
D=M
@ARG
M=D
@endFrame
A=M-1
A=A-1
A=A-1
A=A-1
D=M
@LCL
M=D
@retAddr
A=M
0;JMP
'''

    elif command=="call":
        name=splitted[1]
        nargs=splitted[2]
        return_label=f"{current_function}$ret.{line_number}"
        generated_code=f""""
@{return_label}
D=A
{PUSH_D}
@LCL
D=M
{PUSH_D}
@ARG
D=M
{PUSH_D}
@THIS
D=M
{PUSH_D}
@THAT
D=M
{PUSH_D}
@{nargs}
D=A
@5
D=D+A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@{name}
0;JMP
({return_label})
"""

    return comment+generated_code

BOOTSTRAP=f"""@256
D=A
@SP
M=D
// call Sys.init 0"
@bootstrap$$ret
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@5
D=D+A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.init
0;JMP
(bootstrap$$ret)
"""


class VMTranslator:
    def __init__(self,path: Path):
        self.accumulated_line_number=0
        self.translate(path)

    def translate(self,path: Path):
            if path.is_dir():
                with open(path/f"{path.stem}.asm", "w") as asm:
                    asm.write(BOOTSTRAP)
                    for file in path.glob("*.vm"):
                        self.translate_file(file,asm)
            elif path.is_file():
                with open(path.with_suffix(".asm"), "w") as asm:
                    self.translate_file(path,asm)
            else:
                raise ValueError("should never reach here (unless the path passed is not file nor dir)")
    

    def translate_file(self,path: Path, asm:TextIOWrapper):
        self.current_function=None
        with open(path) as vm:
            for line in vm:
                self._set_current_function_if_necessary(line)
                translated=translate_line(line,self.accumulated_line_number,path.stem,self.current_function)
                if translated is not None:
                    asm.write(f"{translated}\n")
                    self.accumulated_line_number+=1

    def _set_current_function_if_necessary(self,line:str)->None:
        splitted=line.split()
        if splitted and splitted[0]=="function":
            self.current_function=splitted[1]

def main():
    VMTranslator(Path(sys.argv[1]))

if __name__ == '__main__':
    main()