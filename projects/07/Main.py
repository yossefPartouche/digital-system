import os
import sys


class VmTranslator:
    def __init__(self):
        self.static = "@16"
        self.temp = "@5"
        self.eq_count = 0
        self.gt_count = 0
        self.lt_count = 0
        self.count = 0
        self.labels = {}
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
    def assemble_if_goto(self, label_name):
        return ["@" + self.labels.get(label_name), "D;JLT"]
    def assemble_goto(self, label_name):
        return ["@" + self.labels.get(label_name), "0;JMP"]

    def assemble_label(self, label_name: str):
        return ["(" + self.labels.get(label_name) + ")"]

    # potentialy at to the parameter a return adrress

    def assemble_call(self, function_name, num_args):
        return [
            # Not to sure if return address has to be changed to something unique
            "@return_address", "D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1",
            # Save LCL, ARG, THIS, THAT
            "@LCL", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1",
            "@ARG", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1",
            "@THIS", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1",
            "@THAT", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1",
            # Reposition ARG for the called function
            "@SP", "D=M", f"@{num_args + 5}", "D=D-A", "@ARG", "M=D",
            # Reposition LCL for the called function
            "@SP", "D=M", "@LCL", "M=D",
            # Jump to function
            f'@{function_name}', "0;JMP",
            # Define return address label
            "(return_address)"
        ]
    def assemble_function(self, function_name, num_args):
        return [
            "(" + self.labels.get(function_name) + ")",
            # stores the number of arguments in the stack of the frame
            "@num_args", "D=A", "@SP", "A=M", "M=D",
            # Setting the local pointer segment to that of the SP before commencing of the function
            "@SP", "D=M", "@LCL", "M=D",
            # Push num_args 0 values to initialise the callee
            # we create a small loop to do this
            "(init_locals_loop)", "num_args", "D=A",
            "@init_locals_end", "D;JEQ",
            "@SP", "A=M", "M=0", "@SP", "M=M+1",
            "@" + num_args, "M=M-1",
            "@init_locals_loop", "0;JMP",
            "(" + "init_locals_end" + ")"
        ]

    def assemble_return(self):
        return [
            # RAM[LCL] => RAM[13]
            "@LCL", "D=M", "@13", "M=D",
            # string return address
            # RAM[13] => RAM[14]
            "@13", "D=M", "@14", "M=D",
            # RAM[14] = RAM[14] -5
            "@5", "D=A", "@14", "M=M-D",
            "A=M", "D=M", "@14", "M=D",
            # RAM[SP] = RAM[SP] -1
            "@SP", "M=M-1",
            # RAM[RAM[SP]] = RAM[RAM[ARG]]
            "A=M", "D=M",
            # ^^^^ obtained RAM[RAM[SP]]
            "@ARG", "A=M", "M=D",
            # converting back RAM[SP] to caller frame
            "@ARG", "M=M+1", "D=M", "@SP", "M=D",
            # //duplicating the value at RAM[13] in RAM[15]
            "@ 13", "D=M", "@15", "M=D",
            # Return LCL, ARG, THIS, THAT, to caller Frame
            "@15", "M=M-1", "A=M", "D=M", "@THAT", "M=D",
            "@15", "M=M-1", "A=M", "D=M", "@THIS", "M=D",
            "@15", "M=M-1", "A=M", "D=M", "@ARG", "M=D",
            "@15", "M=M-1", "A=M", "D=M", "@LCL", "M=D",
            # goto return address
            "@13", "A=M", "0;JMP"
        ]

    def process_read_line(self, line, output_path):
        assemble = []
        vm_line_part = line.split()
        command_type = translate.command_type(vm_line_part[0])
        if len(vm_line_part) > 1:
            actions = {
                "C_PUSH": self.assemble_push,
                "C_POP": self.assemble_pop,
            }
            a_command = actions.get(command_type)
            assemble = a_command(vm_line_part)
            self.process_write_line(line, assemble, output_path)
        if line.startswith("label"):
            self.process_write_line(line, self.assemble_label(vm_line_part[1]), output_path)
        elif line.startswith("goto"):
            self.process_write_line(line, self.assemble_goto(vm_line_part[1]), output_path)
        elif line.startswith("if-goto"):
            self.process_write_line(line, self.assemble_if_goto(vm_line_part[1]), output_path)
        elif line.startwith("function"):
            self.process_write_line(line, self.assemble_if_goto(vm_line_part[1], vm_line_part[2]), output_path)
        elif line.startswith("call"):
            self.process_write_line(line, self.assemble_call(vm_line_part[1], vm_line_part[2]), output_path)
        elif line.strip() == "gt":
            self.process_write_line(line, self.assemble_gt(), output_path)
        elif line.strip() == "lt":
            self.process_write_line(line, self.assemble_lt(), output_path)
        elif line.strip() == "eq":
            self.process_write_line(line, self.assemble_eq(), output_path)
        elif line.strip() == "return":
            self.process_write_line(line, self.assemble_return(), output_path)
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
        with (open(input_path, "r") as vm_file):
            for line in vm_file:
                line = line.strip()
                if line and not line.startswith("//"):
                    if line.startswith("label") or line.startswith("function"):
                        translate.count += 1
                        line_in_parts = line.split()
                        label_name = line_in_parts[1].upper() + "_" + str(translate.count)
                        translate.labels[line_in_parts[1]] = label_name
            for line in vm_file:
                line = line.strip()
                if line and not line.startswith("//"):
                    translate.process_read_line(line, output_path)
    #THE SAME CONCEPT AS ABOVE NEEDS TO BE DEALTH WITH
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
