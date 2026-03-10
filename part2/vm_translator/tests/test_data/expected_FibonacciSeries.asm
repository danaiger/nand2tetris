//(0) push argument 1
@ARG
D=M
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
//(1) pop pointer 1
@SP
M=M-1
A=M
D=M
@THAT
M=D
//(2) push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
//(3) pop that 0
@THAT
D=M
@0
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
M=M-1
//(4) push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
//(5) pop that 1
@THAT
D=M
@1
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
M=M-1
//(6) push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
//(7) push constant 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
//(8) sub
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
M=M+1
//(9) pop argument 0
@ARG
D=M
@0
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
M=M-1
//(10) label LOOP
(LOOP)
//(11) push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
//(12) if-goto COMPUTE_ELEMENT
@SP
M=M-1
A=M
D=M
@COMPUTE_ELEMENT
D;JGT
//(13) goto END
@END
0;JMP
//(14) label COMPUTE_ELEMENT
(COMPUTE_ELEMENT)
//(15) push that 0
@THAT
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
//(16) push that 1
@THAT
D=M
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
//(17) add
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
//(18) pop that 2
@THAT
D=M
@2
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
M=M-1
//(19) push pointer 1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
//(20) push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
//(21) add
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
//(22) pop pointer 1
@SP
M=M-1
A=M
D=M
@THAT
M=D
//(23) push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
//(24) push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
//(25) sub
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
M=M+1
//(26) pop argument 0
@ARG
D=M
@0
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
M=M-1
//(27) goto LOOP
@LOOP
0;JMP
//(28) label END
(END)
