import sys
import os

sys.path.append(
    f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/src"
)

import make_rca


def test_make_instance_bbox_input():
    output_prefix = "tests/test_make_instance_bbox_input"
    instance_cell_path_file = "tests/test_make_cell_path.inst.cell.path.txt"
    instance_current_file = "tests/test.i.txt"
    #
    args = f"make_cell_path.py {output_prefix} {instance_cell_path_file} {instance_current_file}"
    #
    my_make_cell_path = make_rca.MakeInstanceBBOXInput()
    my_make_cell_path.run(args.split())


if __name__ == "__main__":
    test_make_instance_bbox_input()
