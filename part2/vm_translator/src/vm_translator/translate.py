def translate_line(line:str)->str:
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

    return comment+generated_code
