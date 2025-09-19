import sys
import argparse


class Instance:
    def __init__(self, name=""):
        self.m_name = name
        self.m_cell = None

    def set_name(self, name):
        self.m_name = name

    def get_name(self):
        return self.m_name

    def set_cell(self, cell):
        self.m_cell = cell

    def get_cell(self):
        return self.m_cell


class Cell:
    def __init__(self, name="", subckt=True):
        self.m_name = name
        self.m_instance_dic = {}
        self.m_subckt = subckt

    def set_name(self, name):
        self.m_name = name

    def get_name(self):
        return self.m_name

    def add_instance(self, inst):
        if not inst.get_name() in self.m_instance_dic:
            self.m_instance_dic[inst.get_name()] = inst

    def get_instance_dic(self):
        return self.m_instance_dic

    def set_subckt(self, subckt):
        self.m_subckt = subckt

    def get_subckt(self):
        return self.m_subckt


class MakeCellPath:
    def __init__(self):
        self.m_version = "20250919.0.0"
        self.m_argparser = argparse.ArgumentParser()
        self.m_output_prefix = ""
        self.m_top_cell_name = ""
        self.m_ckt_file_name = ""
        self.m_skip_cell_names = []
        #
        self.m_current_cell = None
        self.m_cell_dic = {}
        self.m_cell_paths = []

    # def print_usage(self):
    #    print(f"make_cell_path.py({self.m_version}) usage:")
    #    print(
    #        f"make_cell_path.py output_prefix top_cell ckt_file <--skip_cells cell1 cell2 ... cellN>"
    #    )

    def read_args(self, args):
        print(f"# read args start")
        self.m_argparser.add_argument(
            "output_prefix", type=str, help="output prefix"
        )
        self.m_argparser.add_argument(
            "top_cell", type=str, help="top cell name in ckt_file"
        )
        self.m_argparser.add_argument("ckt_file", type=str, help="ckt file")
        self.m_argparser.add_argument(
            "--skip_cells", type=str, nargs="+", help="skip cell names"
        )
        #
        args = self.m_argparser.parse_args(args[1:])
        #
        self.m_output_prefix = args.output_prefix
        self.m_top_cell_name = args.top_cell
        self.m_ckt_file_name = args.ckt_file
        if args.skip_cells:
            self.m_skip_cell_names = args.skip_cells
        #
        print(f"# read args end")

    def print_inputs(self):
        print(f"# print inputs start")
        print(f"output prefix : {self.m_output_prefix}")
        print(f"top cell      : {self.m_top_cell_name}")
        print(f"ckt file      : {self.m_ckt_file_name}")
        for skip_cell_name in self.m_skip_cell_names:
            print(f"skip cells    : {skip_cell_name}")
        print(f"# print inputs end")

    def read_ckt_file(self):
        print(f"# read ckt file({self.m_ckt_file_name}) start")
        nlines = 0
        total_line = ""
        f = open(self.m_ckt_file_name, "rt")
        while True:
            line = f.readline()
            nlines += 1
            if not line:
                break
            #
            if 0 == (nlines % 1000000):
                print(f"{nlines} lines")
            #
            line1 = line.strip()
            if 0 == len(line1):
                continue
            #
            if "+" == line1[0]:
                total_line += line[1:]
            else:
                self.read_total_line(total_line)
                total_line = line
        self.read_total_line(total_line)
        print(f"{nlines} lines")
        f.close()
        print(f"# read ckt file({self.m_ckt_file_name}) end")

    def read_total_line(self, total_line):
        tokens = total_line.split()
        if 0 == len(tokens):
            return
        #
        if ".subckt" == tokens[0].lower():
            if not tokens[1] in self.m_cell_dic:
                self.m_current_cell = Cell(tokens[1], True)
                self.m_cell_dic[tokens[1]] = self.m_current_cell
            else:
                self.m_current_cell = self.m_cell_dic[tokens[1]]
        elif ".ends" == tokens[0].lower():
            self.m_current_cell = None
        elif "x" == tokens[0].lower()[0]:
            instance = Instance(tokens[0])
            self.m_current_cell.add_instance(instance)
            if tokens[-1] in self.m_cell_dic:
                cell = self.m_cell_dic[tokens[-1]]
                instance.set_cell(cell)
            else:
                cell = Cell(tokens[-1], True)
                self.m_cell_dic[tokens[-1]] = cell
                instance.set_cell(cell)
        # mname n1 n2 n3 n4 model ...
        elif "m" == tokens[0].lower()[0]:
            instance = Instance(tokens[0])
            self.m_current_cell.add_instance(instance)
            if tokens[5] in self.m_cell_dic:
                cell = self.m_cell_dic[tokens[5]]
                instance.set_cell(cell)
            else:
                cell = Cell(tokens[5], False)
                self.m_cell_dic[tokens[5]] = cell
                instance.set_cell(cell)
        # dname n1 n2 model ...
        elif "d" == tokens[0].lower()[0]:
            instance = Instance(tokens[0])
            self.m_current_cell.add_instance(instance)
            if tokens[3] in self.m_cell_dic:
                cell = self.m_cell_dic[tokens[3]]
                instance.set_cell(cell)
            else:
                cell = Cell(tokens[3], False)
                self.m_cell_dic[tokens[3]] = cell
                instance.set_cell(cell)
        # qname n1 n2 n3 model ...
        elif "q" == tokens[0].lower()[0]:
            instance = Instance(tokens[0])
            self.m_current_cell.add_instance(instance)
            if tokens[4] in self.m_cell_dic:
                cell = self.m_cell_dic[tokens[4]]
                instance.set_cell(cell)
            else:
                cell = Cell(tokens[4], False)
                self.m_cell_dic[tokens[4]] = cell
                instance.set_cell(cell)
        elif "r" == tokens[0].lower()[0]:
            instance = Instance(tokens[0])
            self.m_current_cell.add_instance(instance)
            if "R" in self.m_cell_dic:
                cell = self.m_cell_dic["R"]
                instance.set_cell(cell)
            else:
                cell = Cell("R", False)
                self.m_cell_dic["R"] = cell
                instance.set_cell(cell)
        elif "l" == tokens[0].lower()[0]:
            instance = Instance(tokens[0])
            self.m_current_cell.add_instance(instance)
            if "L" in self.m_cell_dic:
                cell = self.m_cell_dic["L"]
                instance.set_cell(cell)
            else:
                cell = Cell("L", False)
                self.m_cell_dic["L"] = cell
                instance.set_cell(cell)
        elif "c" == tokens[0].lower()[0]:
            instance = Instance(tokens[0])
            self.m_current_cell.add_instance(instance)
            if "C" in self.m_cell_dic:
                cell = self.m_cell_dic["C"]
                instance.set_cell(cell)
            else:
                cell = Cell("C", False)
                self.m_cell_dic["C"] = cell
                instance.set_cell(cell)
        else:
            pass

    def write_inst_cell_path_file(self):
        file_name = f"{self.m_output_prefix}.inst.cell.path.txt"
        print(f"# write inst_cell_path file({file_name}) start")
        f = open(file_name, "wt")
        if self.m_top_cell_name in self.m_cell_dic:
            top_cell = self.m_cell_dic[self.m_top_cell_name]
            self.write_inst_cell_path_file_recursive(top_cell, "", "", 0, f)
        else:
            print(f"# error : top cell({self.m_top_cell_name}) is not found!")
            exit(0)
        f.close()
        print(f"# write inst_cell_path file({file_name}) end")

    def write_inst_cell_path_file_recursive(
        self, parent_cell, parent_instance_path, parent_cell_path, hier_level, f
    ):
        if parent_cell.get_name() in self.m_skip_cell_names:
            return
        #
        for instance_name in parent_cell.get_instance_dic():
            instance = parent_cell.get_instance_dic()[instance_name]
            cell = instance.get_cell()
            #
            parent_instance_path_1 = instance.get_name()
            parent_cell_path_1 = cell.get_name()
            if 0 < hier_level:
                parent_instance_path_1 = (
                    f"{parent_instance_path}.{instance.get_name()}"
                )
                parent_cell_path_1 = f"{parent_cell_path}.{cell.get_name()}"
            #
            if False == cell.get_subckt():
                f.write(f"{parent_instance_path_1} $ {parent_cell_path_1}\n")
                self.m_cell_paths.append(parent_cell_path_1)
            else:
                #
                self.write_inst_cell_path_file_recursive(
                    cell,
                    parent_instance_path_1,
                    parent_cell_path_1,
                    hier_level + 1,
                    f,
                )

    def write_cell_path_file(self):
        file_name = f"{self.m_output_prefix}.cell.path.txt"
        print(f"# write cell_path file({file_name}) start")
        unique_set = set(self.m_cell_paths)
        unique_list = list(unique_set)
        f = open(file_name, "wt")
        for cell_path in unique_list:
            f.write(f"{cell_path}\n")
        f.close()
        print(f"# write cell_path file({file_name}) end")

    def run(self, args):
        print(f"# make_cell_path.py({self.m_version}) start")
        self.read_args(args)
        self.print_inputs()
        self.read_ckt_file()
        self.write_inst_cell_path_file()
        print(f"# make_cell_path.py({self.m_version}) end")


def main(args):
    my_make_cell_path = MakeCellPath()
    my_make_cell_path.run(args)


if __name__ == "__main__":
    main(sys.argv)
