import os
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


    def process_read_line(self, input_file):
        pass

    def process_write_line(self):
        pass

def main():

    translate_vm = VmTranslator()

    if input_file := sys.argv and len(sys.argv) >= 2:
        translate_vm.process_read_line(input_file)
    else:
        print("Usage: python script_name.py filename")
        sys.exit(1)




if __name__ == "__main__":
    # This block will only execute when the script is run directly
    main()
