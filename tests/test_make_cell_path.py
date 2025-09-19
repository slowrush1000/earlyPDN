import sys
import os

sys.path.append(
    f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/src"
)

import make_cell_path


def test_make_cell_path():
    output_prefix = "tests/test_make_cell_path"
    top_cell = "TOP"
    ckt_file = "tests/test.ckt"
    skip_cells = "--skip_cells A B C"
    #
    args = (
        f"make_cell_path.py {output_prefix} {top_cell} {ckt_file} {skip_cells}"
        # f"make_cell_path.py {output_prefix} {top_cell} {ckt_file}"
    )
    #
    my_make_cell_path = make_cell_path.MakeCellPath()
    my_make_cell_path.run(args.split())


if __name__ == "__main__":
    test_make_cell_path()
