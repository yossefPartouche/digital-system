import sys
import os

class address_dictionary:
    def __init__(self):
        self.data = {}
        self.counter = 15
        self.special_cases = {
            **{f"@R{i}": str(i) for i in range(16)},
            "@SCREEN": "16384",
            "@KBD": "24576" 
        }
    def __getitem__(self, key):
        if key in self.special_cases:
            return self.data.setdefault(key, self.special_cases[key])
        elif key.startswith("@"):
            self.counter += 1
            return self.data.setdefault(key, str(self.counter))
class operation: 
    def __init__(self):
        self.destinationTable = {
            "": "000",
            "M": "001",
            "D": "010",
            "DM": "011",
            "A": "100",
            "AM": "101",
            "AD": "110",
            "AMD": "111"
        }

        self.jumpTable = {
            "": "000",
            "JGT": "001",
            "JEQ": "010",
            "JGE": "011",
            "JLT": "100",
            "JNE": "101",
            "JLE": "110",
            "JMP": "111"
        }
        #compute := "_" : "(111) (0 or 1) _ _ _ _ _ _ "
        self.compTable = {
            # where a=0
            #comnpute : "_" : "(111) (0) _ _ _ _ _ _ "
            "0": "1110101010",
            "1": "1110111111",
            "-1": "1110111010",
            "D": "1110001100",
            "A": "1110110000",
            "!D": "1110001101",
            "!A": "1110110001",
            "-D": "1110001111",
            "-A": "1110110011",
            "D+1": "1110011111",
            "A+1": "1110110111",
            "D-1": "1110001110",
            "A-1": "1110110010",
            "D+A": "1110000010",
            "D-A": "1110010011",
            "A-D": "1110000111",
            "D&A": "1110000000",
            "D|A": "1110010101",

            #where a=1
            #compute := "_" : "(111) (1)  _ _ _ _ _ _ "

            "M": "1111110000",
            "!M": "1111110001",
            "-M": "1111110011",
            "M+1": "1111110111",
            "M-1": "1111110010",
            "D+M": "1111000010",
            "D-M": "1111010011",
            "M-D": "1111000111",
            "D&M": "1111000000",
            "D|M": "1111010101"
        }
def extract_instruction(instruction):
    # Split the instruction by '=' to separate destination and the rest
    parts = instruction.split('=')
    
    # Extract the destination (if present)
    dest = parts[0].strip() if len(parts) > 1 else ""
    
    # Split the rest by ';' to separate computation and jump (if present)
    if len(parts) > 1:
        comp_jump = parts[1].split(';')
        comp = comp_jump[0].strip()
        jump = comp_jump[1].strip() if len(comp_jump) > 1 else ""
    else:
        # No '=' found, treat the whole instruction as computation (comp)
        comp_jump = instruction.split(';')
        comp = comp_jump[0].strip()
        jump = comp_jump[1].strip() if len(comp_jump) > 1 else ""
    
    return dest, comp, jump

def to_16_bit(number):
        return format(number, '016b')
class Parsing:
    #conversion for the address
    def to_16_bit(number):
        return format(number, '016b')

    if len(sys.argv) < 2:
        print("Usage: python script_name.py filename")
        sys.exit(1)
    with open(sys.argv[1], "r") as input_file, open("temp_output.txt", "w") as temp_output_file:
        for line in input_file:
            if (not line.strip().startswith("//") 
                and line.strip() != ""              
                and not line.strip().isspace()     
                and not line.strip().startswith("(")):
                temp_output_file.write(line) #writes to our output_file each line seperate


    with open("temp_output.txt", "r+") as temp_output_file, open("output_file.txt", "w") as output_file:
        address = address_dictionary()
        operate = operation()
        for line in temp_output_file:
            if line.startswith("@"):
                key = line.strip()
                value = address.__getitem__(key)
                #trial for direct conversions          
                output_file.write(str(to_16_bit(int(value)))  + "\n")
            else:
                dest, comp, jump = extract_instruction(line) 
                comp = operate.compTable.get(comp)
                dest = operate.destinationTable.get(dest)
                jump = operate.jumpTable.get(jump)
                output_file.write(str(comp)+str(dest)+str(jump) + "\n")