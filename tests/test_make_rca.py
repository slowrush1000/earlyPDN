import sys
import os

sys.path.append(
    f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/src"
)

import make_rca


def test_make_rca():
    output_prefix = "tests/test_make_rca"
    instance_bbox_file = "tests/test.instance.bbox.txt"
    instance_current_file = "tests/test.i.txt"
    layer = "BP"
    net = "VDD"
    level = "--level 0"
    #
    # args = f"make_cell_path.py {output_prefix} {instance_bbox_file} {instance_current_file} {layer} {net} {level}"
    args = f"make_cell_path.py {output_prefix} {instance_bbox_file} {instance_current_file} {layer} {net}"
    #
    my_make_cell_path = make_rca.MakeRCA()
    my_make_cell_path.run(args.split())


if __name__ == "__main__":
    test_make_rca()
