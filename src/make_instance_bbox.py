import sys
import os
import argparse


class MakeInstanceBBOX:
    def __init__(self):
        self.m_output_prefix = ""
        self.m_library = ""
        self.m_cell = ""
        self.m_shrink_factor = "1.0"
        self.m_instance_bbox_file_name = ""

    def read_args(self, args):
        print(f"# read args start")
        self.m_argparser.add_argument(
            "output_prefix", type=str, help="output prefix"
        )
        self.m_argparser.add_argument("library", type=str, help="vse library")
        self.m_argparser.add_argument("cell", type=str, help="vse cell")
        self.m_argparser.add_argument(
            "shrink_factor", type=str, help="shrink factor"
        )
        #
        args = self.m_argparser.parse_args(args[1:])
        #
        self.m_output_prefix = args.output_prefix
        self.m_library = args.library
        self.m_cell = args.cell
        self.m_shrink_factor = args.shrink_factor
        #
        print(f"# read args end")

    def print_inputs(self):
        print(f"# print inputs start")
        print(f"output prefix           : {self.m_output_prefix}")
        print(f"library                 : {self.m_library}")
        print(f"cell                    : {self.m_cell}")
        print(f"shrink factor           : {self.m_shrink_factor}")
        print(f"# print inputs end")

    def run_vse_skill(self):
        print(f"# run vse skill start")
        print(f"# run vse skill end")

    def move_instance_bbox_file(self):
        print(f"# move instance bbox file start")
        if os.path.exists(self.m_instance_bbox_file_name):
            file_name = (
                f"{self.m_instance_bbox_file_name}.{self.m_output_prefix}.txt"
            )
            os.rename(self.m_instance_bbox_file_name, file_name)
        print(f"# move instance bbox file end")


def main(args):
    my_make_instance_bbox = MakeInstanceBBOX()
    my_make_instance_bbox.run(args)


if __name__ == "__main__":
    main(sys.argv)
