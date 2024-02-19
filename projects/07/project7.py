import sys


class VmTranslator:
    def __init__(self):

        self.commandType = {
            "push": "C_PUSH", "pop": "C_POP", "add": "C_ARITHMATIC", "sub": "C_ARITHMATIC",
            "neg": "C_ARITHMATIC", "eq": "C_ARITHMATIC", "gt": "C_ARITHMATIC", "lt": "C_ARITHMATIC",
            "and": "C_ARITHMATIC", "or": "C_ARITHMATIC", "not": "C_ARITHMATIC", "label": "symbol n",
            "goto": "symbol", "if-goto": "symbol", "function" : "symbol n", "call": "symbol n", "return": "return"
    }

    # checks for more lines in the input

    def has_more_lines(self):
        pass

    # Advances to the next line of the file
    # Applied when has_more_lines returns true

    def advance(self):
        pass

    # checks whether the command type of Arithmetic or Push/Pop or otherwiseS

    def command_type(self, command :str):

        return self.commandType.get(command)



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
    def assemble_push(self, line_in_parts):
        value = line_in_parts[2]
        if line_in_parts[1] == "constant":
            return ["@"+value,"D=A", "@SP", "A=M", "M=D", "@SP","M=M+1"]
        elif line_in_parts[1] == "local":
            return []
        elif line_in_parts[1] == "argument":
            return []
        elif line_in_parts[1] == "static":
            return []
        elif line_in_parts[1] == "pointer":
            return []
        elif line_in_parts[1] == "argument":
            return []
        elif line_in_parts[1] == "this":
            return []
        elif line_in_parts[1] == "that":
            return []
        # we are dealing with a temp case
        # IMPLEMENT HERE
        return []

    def assemble_pop(self, line_in_parts):

        return "string"

    def assemble_arithmetic(self, line_in_parts):

        return "string"

    def assemble_symbol_n(self, line_in_parts):
        return "string"

    def assemble_symbol(self, line_in_parts):
        return "string"

    def assemble_return(self, line_in_parts):
        return "string"

    def process_read_line(self, line):
        if not line.startswith("//") and not line.strip() == "":
            vm_line_part = line.split()
            command_type = translate.command_type(vm_line_part[0])
            if command_type:
                actions = {
                    "C_PUSH": self.assemble_push,
                    "C_POP": self.assemble_pop,
                    "C_ARITHMATIC": self.assemble_arithmetic,
                    "symbol": self.assemble_symbol,
                    "symbol_n": self.assemble_symbol_n
                }
                action = actions.get(command_type)
                if action:
                    assembled = action(vm_line_part)
                    self.process_write_line(line, assembled)
        return

    def process_write_line(self, line, assembled_line):

        with open("file.asm", "a") as out_file:
            out_file.write("//" + line + "\n")
            out_file.write(assembled_line + "\n")

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
