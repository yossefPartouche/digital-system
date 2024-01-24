// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen
// by writing 'black' in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen by writing
// 'white' in every pixel;
// the screen should remain fully clear as long as no key is pressed.

//RAM[24576] = KEYBOARD 

//R0=16384//
@16384	//This is reffering to a memory slot
D=A	//we now say the Adress/Memory slot called 16384 is now being considered as a number
@R0	//This is reffering to a memory slot
M=D	//We now say the memory of R0 will contain data=16384

//R1=16384//
@16384
D=A
@R2
M=D

//i=0//
@i
M=0

//j=0//
@j
M=0

//If RAM[24576] == 0 --> NO Keys are being pressed//
(LOOP)
@24576 //This is reffering to a memory slot
D=M  //Load value at RAM[24576] into a Data
@NO_KEYS_PRESS
D;JEQ	//Jump to  NO_KEYS_PRESS if D (value at RAM[24576]) is equal to zero

//Otherwise keys are being pressed//
@R2
D=M
@j
A=D+M
M=-1

//j=j+1//
@j
M=M+1
//goto Loop
@LOOP
0;JMP

(NO_KEYS_PRESS)
@R0
D=M	//transfer data stored in the memory to the Data - register (to be used)
@i	
A=D+M	//Adress = (Data stored in R0) + (Memory stored at i) 
M=0	//memory will be turn to -1

//i=i+1//
@i
M=M+1
//goto Loop
@LOOP
0;JMP

