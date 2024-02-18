import sys


class VmTranslator:

    # checks for more lines in the input

    def has_more_lines(self):
        pass

    # Advances to the next line of the file
    # Applied when has_more_lines returns true

    def advance(self):
        pass

    # checks whether the command type of Arithmetic or Push/Pop

    def command_type(self):
        pass

    # returns the first argument of the current command
    # i.e. C_ARITHMETIC returns (add, sub, lt, gt etc.)
    # IMPORTANT: not to be called if the current command is C_COMMAND

    def arg1(self):
        pass

    # returns the second argument of the current command
    # parameters: command_type = C_PUSH, C_POP, C_FUNCTION or C_CALL
    def arg2(self):
        pass

    # Writes to the output file the Assembly equivalent of code
    # Arithmatic/logical commands
    def write_arithmatic(self, command_type_a):
        pass

    # Writes to the output file the Assembly equivalent of code:
    # of pop and push commands
    def write_push_pop(self, command_type_p):
        pass

    def process_read_line(self, line):
        if not line.startswith("//") and not line.strip() == "":
            translate.process_write_line(line)

    def process_write_line(self, line):

        with open("file.asm", "a") as out_file:
            out_file.write("//" + line + "\n")


translate = VmTranslator()


def main():

    if len(sys.argv) >= 2:
        with open(sys.argv[1], "r") as in_file:
            for line in in_file:
                line.strip()
                translate.process_read_line(line)

    else:
        print("Usage: python script_name.py filename")
        sys.exit(1)


if __name__ == "__main__":
    # This block will only execute when the script is run directly
    main()
