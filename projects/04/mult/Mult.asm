@R0 //grab me R0
D=M //Its data will be the memory within R0
@i //grab "R16" 
M=D-1 //the value stored inside "R16" will be that of R0


//Makes sure R2=0//
@R2
M=0

(ITERATION)
@i
D=M
@MULTIPLY
D;JGE

@END
0;JMP

(MULTIPLY)
@R1
D=M
@R2
M=M+D
@i
D=M
M=M-1
@ITERATION
0;JMP

(END)
@END
0;JMP
