import sys


class VmTranslator:
    def __init__(self):
        self.rand_count = 0
        self.static = 16
        self.temp = "@5"
        self.eq_count = 0
        self.gt_count = 0
        self.lt_count = 0
        self.count = 0
        self.ret_count = 0
        self.inner_count = 0
        self.labels = {}
        self.fun_name = ""
        self.static_base = {str: int}
        self.current_class = ""
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

    # Writes to the output file the Assembly equivalent of code:
    # of pop and push commands
    def assemble_push(self, line_in_parts):
        i = line_in_parts[2]
        if self.kind.get(line_in_parts[1]):
            return [
                "@" + i, "D=A", "@13", "M=D",
                "@" + self.kind.get(line_in_parts[1]),
                "D=M", "@13", "D=D+M", "A=D", "D=M",
                "@SP", "A=M", "M=D", "@SP", "M=M+1"
            ]
        elif line_in_parts[1] == "constant":
            return ["@" + i, "D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
        elif line_in_parts[1] == "static":
            print("class name: " + self.current_class)
            base = self.static + self.static_base.get(self.current_class)
            print("base of " + self.current_class + ": " + str(base))
            print("pushing out static Number: " + str(int(i) + base))
            print()
            return ["@" + str(int(i) + base), "D=M",
                    "@SP", "A=M", "M=D", "@SP", "M=M+1"]
        elif line_in_parts[1] == "temp":
            return [
                "@" + i, "D=A", self.temp, "D=A+D",
                "A=D", "D=M",
                "@SP", "A=M", "M=D",
                "@SP", "M=M+1"
            ]
        elif line_in_parts[1] == "pointer" and line_in_parts[2] == "0":
            return ["@THIS", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
        else:
            return ["@THAT", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]

    def assemble_pop(self, line_in_parts):
        i = line_in_parts[2]
        if self.kind.get(line_in_parts[1]):
            return [
                "@" + i, "D=A", "@13", "M=D",
                "@" + self.kind.get(line_in_parts[1]),
                "D=M", "@13", "D=D+M", "M=D",
                "@SP", "M=M-1", "A=M", "D=M", "@13", "A=M",
                "M=D"
            ]
        elif line_in_parts[1] == "static":
            # print("Assemble pop: " + str(self.rand_count + self.static))
            print("class name: " + self.current_class)
            base = self.static + self.static_base.get(self.current_class)
            print("base of " + self.current_class + ": " + str(base))
            print("popping in static Number: " + str(int(i) + base))
            print()
            to_ret = ["@SP", "AM=M-1", "D=M", "@" + str(int(i) + base), "M=D"]
            self.rand_count += 1
            return to_ret
        elif line_in_parts[1] == "temp":
            return [
                "@SP", "M=M-1", "A=M", "D=M", "@13", "M=D",
                "@" + i, "D=A", self.temp, "D=A+D", "@14", "M=D",
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
        return ["@SP", "AM=M-1", "@" + self.fun_name + "$" + label_name, "D;JNE"]

    def assemble_goto(self, label_name):
        return ["@" + self.fun_name + "$" + label_name, "0;JMP"]

    def assemble_label(self, label_name: str):
        return ["(" + self.fun_name + "$" + label_name + ")"]

    # potentially at to the parameter a return address

    def assemble_call(self, function_name, num_args):
        self.ret_count += 1
        ret_list = ["@" + self.fun_name + "$ret_" + str(self.ret_count), "D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1"]

        # Save LCL, ARG, THIS, THAT
        for i in ["LCL", "ARG", "THIS", "THAT"]:
            ret_list = ret_list + ["@" + i, "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
        # we are preparing 5 'open slots' before reaching the function
        ret_list = ret_list + ["@SP", "D=M", "@5", "D=D-A"]
        # we prepare another Nargs spots for the arguments
        # to be placed and then store the starting address in RAM[ARG]
        ret_list = ret_list + ["@" + str(num_args), "D=D-A", "@ARG", "M=D"]
        # saving our relative main SP in our LCL to know our return to reference
        ret_list = ret_list + ["@SP", "D=M", "@LCL", "M=D", ]

        return ret_list + ["@" + function_name, "0;JMP", "(" + self.fun_name + "$ret_" + str(self.ret_count) + ")"]

    def assemble_function(self, function_name, num_vars):
        # self.static = self.static + self.rand_count
        # print("Assemble function " + str(self.static))
        self.fun_name = function_name  # this is necessary if WITHIN (i.e. below) a particular function
        class_name = function_name.split(".")[0]
        self.current_class = class_name
        if not self.static_base.__contains__(class_name):
            self.static_base[class_name] = self.rand_count
        # we have another label
        ret_list = ["(" + self.fun_name + ")"]
        for i in range(int(num_vars)):
            ret_list = ret_list + self.assemble_push(["push", "constant", "0"])
        return ret_list

    def assemble_return(self):
        # our local is what stored are return to reference
        return [
            # RAM[LCL] => RAM[13]
            "@LCL", "D=M", "@R11", "M=D",
            # string return address
            "@5", "A=D-A", "D=M", "@R12",
            "M=D", "@ARG", "D=M", "@0", "D=D+A",
            "@R13", "M=D", "@SP", "AM=M-1", "D=M",
            "@R13", "A=M", "M=D", "@ARG", "D=M", "@SP", "M=D+1",
            # Return LCL, ARG, THIS, THAT, to caller Frame
            "@R11", "D=M-1", "AM=D", "D=M", "@THAT", "M=D",
            "@R11", "D=M-1", "AM=D", "D=M", "@THIS", "M=D",
            "@R11", "D=M-1", "AM=D", "D=M", "@ARG", "M=D",
            "@R11", "D=M-1", "AM=D", "D=M", "@LCL", "M=D",
            # goto return address
            "@R12", "A=M", "0;JMP"
        ]

    def process_read_line(self, line, output_path):
        vm_line_part = line.split()
        if line.startswith("pop"):
            self.process_write_line(line, self.assemble_pop(vm_line_part), output_path)
        elif line.startswith("push"):
            self.process_write_line(line, self.assemble_push(vm_line_part), output_path)
        elif line.startswith("label"):
            self.process_write_line(line, self.assemble_label(vm_line_part[1]), output_path)
        elif line.startswith("goto"):
            self.process_write_line(line, self.assemble_goto(vm_line_part[1]), output_path)
        elif line.startswith("if-goto"):
            self.process_write_line(line, self.assemble_if_goto(vm_line_part[1]), output_path)
        elif line.startswith("function"):
            self.process_write_line(line, self.assemble_function(vm_line_part[1], vm_line_part[2]), output_path)
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

    def process_write_line(self, line, assembled_line: [], output_path):
        with open(output_path, "a") as out_file:
            out_file.write("//" + line + "\n")
            for instruction in assembled_line:
                out_file.write(instruction + "\n")


def main():
    translate = VmTranslator()
    input_path = sys.argv[1]  # working_file.vm ou SysWorking.vm
    output_path = "FunctionCalls/StaticsTest/StaticsTest.asm"  # we need to make this automated
    # according to the chosen file provided
    if input_path.startswith("Sys"):
        with open(input_path, "r") as working_file:
            translate.fun_name = "Sys.init"
            translate.process_write_line("SP = 256", ["@256", "D=A", "@SP", "M=D"], output_path)
            translate.process_write_line("Sys.init bootstrap",
                                         translate.assemble_call("Sys.init", 0), output_path)
    with open(input_path, "r") as working_file:
        for line in working_file:
            translate.process_read_line(line, output_path)


if __name__ == "__main__":
    main()
