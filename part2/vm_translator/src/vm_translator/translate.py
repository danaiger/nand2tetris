def translate_line(line:str)->str:
    command,segment,number=line.split(' ')
    return f'''// {command} {segment} {number}
@{number}
D=A
@SP
A=M
M=D
@SP
M=M+1'''
