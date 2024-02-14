import sys
import os

class address_dictionary:
    def __init__(self):
<<<<<<< HEAD
        self.label = {}
        self.counter = 15
        self.variable = {}

        self.special_cases = {
            "@SP":"@0",
            "@LCL":"@1",
            "@ARG":"@2",
            "@THIS":"@3",
            "@THAT":"@4",
            "@R0": "@0",
            "@R1": "@1",
            "@R2": "@2",
            "@R3": "@3",
            "@R4": "@4",
            "@R5": "@5",
            "@R6": "@6",
            "@R7": "@7",
            "@R8": "@8",
            "@R9": "@9",
            "@R10": "@10",
            "@R11": "@11",
            "@R12": "@12",
            "@R13": "@13",
            "@R14": "@14",
            "@R15": "@15",
            "@SCREEN": "@16384",
            "@KBD": "@24576"
        }
    
    def __getitem__(self, key):
        if key in self.special_cases:
            return self.special_cases[key] 
        # Case 3: If key is a number greater than 15
        elif key in self.label:
            return  self.label[key]
        elif key in self.variable:
            return "@" + self.variable[key]
        else:
            try:
                num = int(key[1:])
                self.variable[key] = str(num)
                return "@" + str(num)   # Return the same key     
            except ValueError:
                pass
        # Case 2: if it's a variable (non-lable)
        # Key is a string
            self.counter = self.counter + 1
            self.variable[key] = str(self.counter)
            return "@" + str(self.counter)

=======
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
>>>>>>> 46ad5fbf28c47746ca558fc37a9ba5685aeceab4
class operation: 
    def __init__(self):
        self.destinationTable = {
            "": "000",
            "M": "001",
            "D": "010",
<<<<<<< HEAD
            "MD": "011",
=======
            "DM": "011",
>>>>>>> 46ad5fbf28c47746ca558fc37a9ba5685aeceab4
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

<<<<<<< HEAD

class Parsing:
    """
    if len(sys.argv) < 2:
        print("Usage: python script_name.py filename")
        sys.exit(1)
    name = sys.argv[1].split('.')
    file_name = name[0]
    """
    def to_16_bit(number):
        return format(number, '016b')

    address = address_dictionary()
    operate = operation()

    # Step 1: Process labels and assign line numbers
    with open("Add.asm", "r") as filter_file:
        line_number = 0
        for line in filter_file:
            line = line.strip()
            
            if line.startswith("("):
                label = line[1:-1].strip()  # Strip brackets and whitespace
                address.label["@" + label] = "@" + str(line_number)
                print(label +  "  " +address.__getitem__(label))
                line_number = line_number -1
                print("@END_GT have value " + address.__getitem__("@END_GT"))

            if not (line.startswith("//") or line == "" or line.isspace()):
                line_number +=1

    # Step 4: Convert instructions to machine code
    with open("Add.asm", "r") as temp_output_file, open("Add.hack", "w") as output_file:
        for line in temp_output_file:
            line = line.strip()
            if line.startswith("@"):
                value = address.__getitem__(line.strip())
                num = int(value.lstrip('@'))
                output_file.write(str(to_16_bit(num)) + "\n")
            elif not (line.startswith("//") or line.startswith("(") or line == "" or line.isspace()):
                dest, comp, jump = extract_instruction(line)
                comp = operate.compTable.get(comp)
                dest = operate.destinationTable.get(dest)
                jump = operate.jumpTable.get(jump)
                output_file.write(str(comp) + str(dest) + str(jump) + "\n")
=======
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
>>>>>>> 46ad5fbf28c47746ca558fc37a9ba5685aeceab4
