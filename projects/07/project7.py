import sys


class VmTranslator:
    def __init__(self):
        self.commandType = {
            "push": "C_PUSH", "pop": "C_POP", "add": "C_ARITHMATIC", "sub": "C_ARITHMATIC",
            "neg": "C_ARITHMATIC", "eq": "C_ARITHMATIC", "gt": "C_ARITHMATIC", "lt": "C_ARITHMATIC",
            "and": "C_ARITHMATIC", "or": "C_ARITHMATIC", "not": "C_ARITHMATIC", "label": "symbol n",
            "goto": "symbol", "if-goto": "symbol", "function": "symbol n", "call": "symbol n", "return": "return"
        }
        self.kind = {
            "local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT",
        }
        # Writes to the output file the Assembly equivalent of code
        # Arithmatic/logical commands
        self.assemble_arithmetic = {
            "add": ["@SP", "M=M-1", "A=M", "D=M", "@SP", "M=M-1", "A=M", "M=M+D"],
            "sub": ["@SP", "M=M-1", "A=M", "D=M", "@SP", "M=M-1", "A=M", "M=M-D"],
            "neg": ["@SP", "M=M-1", "A=M", "D=M", "M=!D", "D=M+1", "M=D"],
            "eq": ["@SP", "M=M-1", "A=M", "D=M", "@SP", "M=M-1", "A=M", "D=M-D","@EQUAL", "D;JEQ", "@SP",
                   "A=M", "M=0", "@END_EQ", "0;JMP", "(EQUAL)", "@SP", "A=M", "M=1", "(END_EQ)"],
            "gt": ["@SP", "M=M-1", "A=M", "D=M", "@SP", "M=M-1", "A=M", "D=M-D",
                   "@GT", "D;JGT", "@SP", "A=M", "M=0", "@END_GT", "0;JMP", "(GT)", "@SP", "A=M", "M=1", "(END_GT)"],
            "lt": ["@SP", "M=M-1", "A=M", "D=M", "@SP", "M=M-1", "A=M", "D=M-D",
                   "@LT", "D;JLT", "@SP", "A=M", "M=0", "@END_LT", "0;JMP", "(LT)", "@SP", "A=M", "M=1", "(END_LT)"],
            "and": ["@SP", "M=M-1", "A=M", "D=M", "@SP", "M=M-1", "A=M", "D=M&D"],
            "or": ["@SP", "M=M-1", "A=M", "D=M", "@SP", "M=M-1", "A=M", "D=M|D"],
            "not": ["@SP", "M=M-1", "A=M", "D=M", "M=!D"],
        }

    # checks for more lines in the input

    def has_more_lines(self):
        pass

    # Advances to the next line of the file
    # Applied when has_more_lines returns true

    def advance(self):
        pass

    # checks whether the command type of Arithmetic or Push/Pop or otherwiseS

    def command_type(self, command: str):

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

    # Writes to the output file the Assembly equivalent of code:
    # of pop and push commands
    def assemble_push(self, line_in_parts: []):
        if self.kind.get(line_in_parts[1]):
            return ["@"+line_in_parts[2], "D=A", "@13", "M=D", "@"+self.kind.get(line_in_parts[1]), "D=M", "@13", "D=D+M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
        value = line_in_parts[2]
        if line_in_parts[1] == "constant":
            return ["@" + value, "D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
        elif line_in_parts[1] == "static":
            return []
        elif line_in_parts[1] == "pointer":
            return []
        # we are dealing with a temp case
        # IMPLEMENT HERE
        return []

    def assemble_pop(self, line_in_parts: []):
        if self.kind.get(line_in_parts[1]):
            return ["@" + line_in_parts[2], "D=A", "@13", "M=D", "@" + self.kind.get(line_in_parts[1]), "D=M", "@13",
                    "D=D+M", "M=D", "@SP", "M=M-1", "D=M", "@13", "A=M", "M=D"]

    def assemble_symbol_n(self, line_in_parts : []):
        return []

    def assemble_symbol(self, line_in_parts: []):
        return []

    def assemble_return(self, line_in_parts : []):
        return []

    def process_read_line(self, line):
        assembled =[]
        print(line)
        vm_line_part = line.split()
        command_type = translate.command_type(vm_line_part[0])
        if len(vm_line_part) > 1:
            actions = {
                "C_PUSH": self.assemble_push,
                "C_POP": self.assemble_pop,
                "symbol": self.assemble_symbol,
                "symbol_n": self.assemble_symbol_n
            }
            a_command = actions.get(command_type)
            assembled = a_command(vm_line_part)
            self.process_write_line(line, assembled)
        else:
            arithmetic = self.assemble_arithmetic.get(line)
            self.process_write_line(line, arithmetic)

    def process_write_line(self, line, assembled_line):
        with open("StackArithmetic/SimpleAdd/SimpleAdd.asm", "a") as out_file:
            out_file.write("//" + line + "\n")
            for instruction in assembled_line:
                print(instruction)
                out_file.write(instruction + "\n")


translate = VmTranslator()


def main():
    if len(sys.argv) >= 2:
        with open(sys.argv[1], "r") as in_file:
            for line in in_file:
                line.strip()
                if line is not None and not line.startswith("//") and not line.strip() == "":
                    translate.process_read_line(line)

    else:
        print("Usage: python script_name.py filename")
        sys.exit(1)


if __name__ == "__main__":
    # This block will only execute when the script is run directly
    main()
