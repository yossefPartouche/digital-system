import sys


class VmTranslator:
    def __init__(self):
        self.static = "@16"
        self.temp = 5
        self.eq_count = 0
        self.gt_count = 0
        self.lt_count = 0
        self.commandType = {
            "push": "C_PUSH", "pop": "C_POP", "add": "C_ARITHMATIC", "sub": "C_ARITHMATIC",
            "neg": "C_ARITHMATIC", "eq": "C_ARITHMATIC", "gt": "C_ARITHMATIC", "lt": "C_ARITHMATIC",
            "and": "C_ARITHMATIC", "or": "C_ARITHMATIC", "not": "C_ARITHMATIC", "label": "symbol n",
            "goto": "symbol", "if-goto": "symbol", "function": "symbol n", "call": "symbol n", "return": "return"
        }
        self.kind = {
            "local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT",
        }
        self.assemble_arithmatic = {
            "add": ["@SP", "M=M-1", "A=M", "D=M", "@SP", "M=M-1",
                    "A=M", "M=M+D", "@SP", "M=M+1"],
            "sub": ["@SP", "M=M-1", "A=M", "D=M", "@SP", "M=M-1", "A=M", "M=M-D", "@SP", "M=M+1"],
            "neg": ["@SP", "M=M-1", "A=M", "D=M", "M=-D", "@SP", "M=M+1"],
            "and": ["@SP", "M=M-1", "A=M", "D=M", "@SP", "M=M-1", "A=M", "D=M&D", "@SP", "A=M", "M=D", "@SP", "M=M+1"],
            "or": ["@SP", "M=M-1", "A=M", "D=M", "@SP", "M=M-1", "A=M", "D=M|D", "@SP", "A=M", "M=D", "@SP", "M=M+1"],
            "not": ["@SP", "M=M-1", "A=M", "D=M", "M=!D", "@SP", "M=M+1"],
        }
        # Writes to the output file the Assembly equivalent of code
        # Arithmatic/logical commands

    def assemble_eq(self):
        self.eq_count += 1
        equal_label = f"EQUAL_{self.eq_count}"
        end_label = f"END_EQ_{self.eq_count}"
        return [
            "@SP", "M=M-1", "A=M", "D=M",
            "@SP", "M=M-1", "A=M", "D=M-D",
            f"@{equal_label}", "D;JEQ",
            "@SP", "A=M", "M=0",
            f"@{end_label}", "0;JMP",
            f"({equal_label})", "@SP", "A=M", "M=-1",
            f"({end_label})", "@SP", "M=M+1"
        ]

    def assemble_gt(self):
        self.gt_count +=1
        gt_label = f"GT_{self.gt_count}"
        end_gt_label = f"END_GT_{self.gt_count}"
        return [
            "@SP", "M=M-1", "A=M", "D=M",
            "@SP", "M=M-1", "A=M", "D=M-D",
            f"@{gt_label}", "D;JGT",
            "@SP", "A=M", "M=0",
            f"@{end_gt_label}", "0;JMP",
            f"({gt_label})", "@SP", "A=M", "M=-1",
            f"({end_gt_label})", "@SP", "M=M+1"
        ]

    def assemble_lt(self):
        self.lt_count +=1
        lt_label = f"LT_{self.lt_count}"
        end_lt_label = f"END_LT_{self.lt_count}"
        return [
            "@SP", "M=M-1", "A=M", "D=M",
            "@SP", "M=M-1", "A=M", "D=M-D",
            f"@{lt_label}", "D;JLT",
            "@SP", "A=M", "M=0",
            f"@{end_lt_label}", "0;JMP",
            f"({lt_label})", "@SP", "A=M", "M=-1",
            f"({end_lt_label})", "@SP", "M=M+1"
        ]

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
        i = "@" + line_in_parts[2]
        if self.kind.get(line_in_parts[1]):
            return [i, "D=A", "@13", "M=D", "@"+self.kind.get(line_in_parts[1]),
                    "D=M", "@13", "D=D+M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
        elif line_in_parts[1] == "constant":
            return [i, "D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
        elif line_in_parts[1] == "static":
            return [
                i, "D=A", self.static, "D=A+D",
                "A=D", "D=M",
                "@SP", "A=M", "M=D",
                "@SP", "M=M+1"
            ]
        elif line_in_parts[1] == "temp":
            out = [i, "D=A", "@" + str(self.temp), "A=M", "M=D", "@" + str(self.temp), "M=M+1"]
            self.temp = self.temp + 1
            return out
        elif line_in_parts[1] == "pointer" and line_in_parts[2] == 0:
            return ["@THIS", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
        else:
            return ["@THAT", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]

    def assemble_pop(self, line_in_parts: []):
        i = "@" + line_in_parts[2]
        if self.kind.get(line_in_parts[1]):
            return [i, "D=A", "@13", "M=D", "@" + self.kind.get(line_in_parts[1]), "D=M", "@13",
                    "D=D+M", "M=D", "@SP", "M=M-1", "D=M", "@13", "A=M", "M=D"]
        elif line_in_parts[1] == "static":
            return [
                "@SP", "M=M-1", "A=M", "D=M",
                "@13", "M=D",
                i, "D=A", self.static, "D=A+D",
                "@14", "M=D", "@13", "D=M", "@14", "A=M", "M=D"
            ]

    def assemble_symbol_n(self, line_in_parts : []):
        return []

    def assemble_symbol(self, line_in_parts: []):
        return []

    def assemble_return(self, line_in_parts : []):
        return []

    def process_read_line(self, line):
        assemble =[]
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
            assemble = a_command(vm_line_part)
            self.process_write_line(line, assemble)
        elif line.strip() == "gt":
            self.process_write_line(line,self.assemble_gt())
        elif line.strip() == "lt":
            self.process_write_line(line, self.assemble_lt())
        elif line.strip() == "eq":
            self.process_write_line(line,self.assemble_eq())
        else:
            self.process_write_line(line,self.assemble_arithmatic.get(line.strip()))

    def process_write_line(self, line, assembled_line):
        with open("MemoryAccess/StaticTest/StaticTest.asm", "a") as out_file:
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
