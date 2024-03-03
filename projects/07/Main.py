import os
import sys


class VmTranslator:
    def __init__(self):
        self.static = "@16"
        self.temp = "@5"
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
        self.gt_count += 1
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
        self.lt_count += 1
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
            return [
                i, "D=A", "@13", "M=D",
                "@" + self.kind.get(line_in_parts[1]),
                "D=M", "@13", "D=D+M", "A=D", "D=M",
                "@SP", "A=M", "M=D", "@SP", "M=M+1"
            ]
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
            return [
                i, "D=A", self.temp, "D=A+D",
                "A=D", "D=M",
                "@SP", "A=M", "M=D",
                "@SP", "M=M+1"
            ]
        elif line_in_parts[1] == "pointer" and line_in_parts[2] == "0":
            return ["@THIS", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
        else:
            return ["@THAT", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]

    def assemble_pop(self, line_in_parts: []):
        i = "@" + line_in_parts[2]
        if self.kind.get(line_in_parts[1]):
            return [
                i, "D=A", "@13", "M=D",
                "@" + self.kind.get(line_in_parts[1]),
                "D=M", "@13", "D=D+M", "M=D",
                "@SP", "M=M-1", "A=M", "D=M", "@13", "A=M",
                "M=D"
            ]
        elif line_in_parts[1] == "static":
            return [
                "@SP", "M=M-1", "A=M", "D=M", "@13", "M=D",
                i, "D=A", self.static, "D=A+D", "@14", "M=D",
                "@13", "D=M", "@14", "A=M", "M=D"
            ]
        elif line_in_parts[1] == "temp":
            return [
                "@SP", "M=M-1", "A=M", "D=M", "@13", "M=D",
                i, "D=A", self.temp, "D=A+D", "@14", "M=D",
                "@13", "D=M", "@14", "A=M", "M=D"
            ]
        elif line_in_parts[1] == "pointer" and line_in_parts[2] == "0":
            return [
                "@SP", "M=M-1", "A=M", "D=M", "@THIS", "M=D"
            ]
        else:
            return [
                "@SP", "M=M-1", "A=M", "D=M", "@THAT", "M=D"
            ]

    def assemble_symbol_n(self, line_in_parts: []):
        return []

    def assemble_symbol(self, line_in_parts: []):
        return []

    def assemble_return(self, line_in_parts: []):
        # Stores the memory in the local somewhere temp13
        end_frame = ["@LCL", "D=M", "@13", "M=D"]

        # Calculates the end frame using the value store in temp13
        ret_add = ["@LCL", "D=M", "@14", "M=D", "@5", "D=A", "@14", "M=M-D"]

        # takes the memory in the end-frame and stores it somewhere temp15
        potentially_useful = ["@14", "D=M", "@15", "M=D"]

        # 1) Takes data stored inside temp13 to be an address
        # 2) Then retrieves the data and stores it *at the memory stored within Args*
        # *Taking the data stored within args converting to address and then storing the data inside there
        step_1 = ["@13", "A=M", "D=M", "@ARG", "A=M", "M=D"]
        # Convert SP back to its caller frame by taking data of (args + 1) to be the new value for SP
        sp_conv = ["@ARG", "D=M-1", "@SP", "M=D"]
        # Restore THIS, THAT, ARG, LCL
        # goto retAddr
        return []

    def process_read_line(self, line, output_path):
        assemble = []
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
            self.process_write_line(line, assemble, output_path)
        elif line.strip() == "gt":
            self.process_write_line(line, self.assemble_gt(), output_path)
        elif line.strip() == "lt":
            self.process_write_line(line, self.assemble_lt(), output_path)
        elif line.strip() == "eq":
            self.process_write_line(line, self.assemble_eq(), output_path)
        else:
            self.process_write_line(line, self.assemble_arithmatic.get(line.strip()), output_path)

    def process_write_line(self, line, assembled_line, output_path):
        with open(output_path, "a") as out_file:
            out_file.write("//" + line + "\n")
            for instruction in assembled_line:
                out_file.write(instruction + "\n")


translate = VmTranslator()


def main():
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <input_path>")
        sys.exit(1)

    input_path = sys.argv[1]

    if input_path.endswith('.vm'):  # If the input is a single VM file
        output_path = input_path[:-3] + ".asm"
        with open(input_path, "r") as vm_file:
            for line in vm_file:
                line = line.strip()
                if line and not line.startswith("//"):
                    translate.process_read_line(line, output_path)

    elif os.path.isdir(input_path): # If the input is a directory
        # Process all .vm files in the directory
        for filename in os.listdir(input_path):
            if filename.endswith('.vm'):
                output_file = filename[:-3] + ".asm"
                output_path = os.path.join(input_path, output_file)
                vm_file_path = os.path.join(input_path, filename)
                with open(vm_file_path, "r") as vm_file:
                    for line in vm_file:
                        line = line.strip()
                        if line and not line.startswith("//"):
                            translate.process_read_line(line, output_path)

    else:
        print("Invalid input path:", input_path)
        print("Usage: if you tried to add a directory make sure to add the '/' at the end of the path name")
        print("Or make sure path is from the root")
        sys.exit(1)


if __name__ == "__main__":
    main()
