//(0) push constant 7
@7
D=A
@SP
A=M
M=D
@SP
M=M+1
//(1) push constant 8
@8
D=A
@SP
A=M
M=D
@SP
M=M+1
//(2) add
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
M=M+1
