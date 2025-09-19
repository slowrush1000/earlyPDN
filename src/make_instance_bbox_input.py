import sys
import argparse


class MakeInstanceBBOXInput:
    def __init__(self):
        self.m_version = "20250919.0.0"
        self.m_argparser = argparse.ArgumentParser()
        self.m_output_prefix = ""
        self.m_inst_cell_path_file_name = ""
        self.m_instance_current_file_name = ""
        #
        self.m_instance_cell_dic = {}
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
            "instance_cell_path_file", type=str, help="instance-cell path file"
        )
        self.m_argparser.add_argument(
            "instance_current_file", type=str, help="instance current file"
        )
        #
        args = self.m_argparser.parse_args(args[1:])
        #
        self.m_output_prefix = args.output_prefix
        self.m_inst_cell_path_file_name = args.instance_cell_path_file
        self.m_instance_current_file_name = args.instance_current_file
        #
        print(f"# read args end")

    def print_inputs(self):
        print(f"# print inputs start")
        print(f"output prefix           : {self.m_output_prefix}")
        print(f"instance-cell path file : {self.m_inst_cell_path_file_name}")
        print(f"instance current file   : {self.m_instance_current_file_name}")
        print(f"# print inputs end")

    # instance_path $ cell_path
    def read_instance_cell_path_file(self):
        print(
            f"# read instance_cell path file({self.m_inst_cell_path_file_name}) start"
        )
        nlines = 0
        f = open(self.m_inst_cell_path_file_name, "rt")
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
            tokens = line.split()
            if 3 > len(tokens):
                continue
            instance_path = tokens[0]
            instance_paths = self.get_paths(instance_path)
            cell_path = tokens[2]
            cell_paths = self.get_paths(cell_path)
            #
            for i in range(len(instance_paths)):
                key = instance_paths[i]
                if not key in self.m_instance_cell_dic:
                    self.m_instance_cell_dic[key] = cell_paths[i]
        print(f"{nlines} lines")
        f.close()
        print(
            f"# read instance_cell path file({self.m_inst_cell_path_file_name}) end"
        )

    # instance_path current_A
    def read_instance_current_file(self):
        print(
            f"# read instance current file({self.m_instance_current_file_name}) start"
        )
        nlines = 0
        f = open(self.m_instance_current_file_name, "rt")
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
            tokens = line.split()
            key = tokens[0]
            if key in self.m_instance_cell_dic:
                self.m_cell_paths.append(self.m_instance_cell_dic[key])
        print(f"{nlines} lines")
        f.close()
        print(
            f"# read instance current file({self.m_instance_current_file_name}) end"
        )

    def write_instance_bbox_input_file(self):
        file_name = f"{self.m_output_prefix}.cell.path.txt"
        print(f"# write instance bbox input file({file_name}) start")
        unique_set = set(self.m_cell_paths)
        unique_list = list(unique_set)
        f = open(file_name, "wt")
        for cell_path in unique_list:
            f.write(f"{cell_path}\n")
        f.close()
        print(f"# write instance bbox input file({file_name}) end")

    def get_paths(self, path):
        tokens = path.split(".")
        paths = [""] * len(tokens)
        for i in range(len(tokens)):
            paths[i] = ".".join(tokens[0 : i + 1])
            # print(f"{i} - {paths[i]}")
        return paths

    def run(self, args):
        print(f"# make_instance_bbox_input.py({self.m_version}) start")
        self.read_args(args)
        self.print_inputs()
        self.read_instance_cell_path_file()
        self.read_instance_current_file()
        self.write_instance_bbox_input_file()
        print(f"# make_instance_bbox_input.py({self.m_version}) end")


def main(args):
    my_make_instance_bbox_input = MakeInstanceBBOXInput()
    my_make_instance_bbox_input.run(args)


if __name__ == "__main__":
    main(sys.argv)
