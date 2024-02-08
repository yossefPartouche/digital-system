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
        for line in temp_output_file:
            if line.startswith("@"):
                key = line.strip()
                value = address.__getitem__(key)
                #trial for direct conversions          
                output_file.write(str(to_16_bit(int(value)))  + "\n")
            else:
                output_file.write(line)  