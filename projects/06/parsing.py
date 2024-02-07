import sys

class Parsing:
    if len(sys.argv) < 2:
        print("Usage: python script_name.py filename")
        sys.exit(1)
    with open(sys.argv[1], "r") as input_file, open("output_file.txt", "w") as output_file:
        for line in input_file:
            line = line.partition("//")[0]  # Remove comments
            line = line.strip()  # Remove leading/trailing whitespace
            line = line.replace(" ", "")  # Remove spaces
            output_file.write(line + "\n") #writes to our output_file each line seperate