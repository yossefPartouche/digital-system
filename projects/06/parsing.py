import sys

class address_dictionary:
    def __init__(self):
        self.data = {}
        self.counter = 15

    def __getitem__(self, key):
        if key.startswith("@R"):
            index = int(key[2:])
            if 0 <= index <= 15:
                return "@" + str(index)
        elif key == "SCREEN":
            self.data[key] = "@" + "16384"
            return "@" + "16384"
        elif key == "KBD":
            self.data[key] = "@" + "24576"
            return "@" + "24576"
        elif key.startswith("@"):
            if key not in self.data:
                self.counter += 1
                self.data[key] = "@" + str(self.counter)
            return self.data[key]
        return None

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
                output_file.write(str(to_16_bit(int(value[1::])))  + "\n")
            else:
                output_file.write(line)
                                  