import sys
import argparse


class Point:
    def __init__(self, x=0.0, y=0.0):
        self.m_x = x
        self.m_y = y

    def set_x(self, x):
        self.m_x = x

    def get_x(self):
        return self.m_x

    def set_y(self, y):
        self.m_y = y

    def get_y(self, y):
        return self.m_y

    def get_str(self):
        return f"{self.m_x:.4f} {self.m_y:.4f}"


class Box:
    def __init__(
        self,
        llx=sys.float_info.max,
        lly=sys.float_info.max,
        urx=-sys.float_info.max,
        ury=-sys.float_info.max,
    ):
        self.m_ll = Point(llx, lly)
        self.m_ur = Point(urx, ury)

    def set_ll(self, llx, lly):
        self.m_ll.set_x(llx)
        self.m_ll.get_y(lly)

    def get_ll(self):
        return self.m_ll

    def set_ur(self, urx, ury):
        self.m_ur.set_x(urx)
        self.m_ur.get_y(ury)

    def get_ur(self):
        return self.m_ur

    def update(self, other):
        if other.get_ll().get_x() < self.get_ll().get_x():
            self.get_ll().set_x(other.get_ll().get_x())
        if other.get_ll().get_y() < self.get_ll().get_y():
            self.get_ll().set_y(other.get_ll().get_y())
        if other.get_ur().get_x() > self.get_ur().get_x():
            self.get_ur().set_x(other.get_ur().get_x())
        if other.get_ur().get_y() > self.get_ur().get_y():
            self.get_ur().set_y(other.get_ur().get_y())

    def get_str(self):
        return f"{self.m_ll.get_str()} {self.m_ur.get_str()}"


class Instance:
    def __init__(
        self,
        hier_level=-1,
        name="",
        current_A=0.0,
        llx=-sys.float_info.max,
        lly=-sys.float_info.max,
        urx=sys.float_info.max,
        ury=sys.float_info.max,
        parent=None,
    ):
        self.m_hier_level = hier_level
        self.m_name = name
        self.m_current_A = current_A
        #
        self.m_box = Box(llx, lly, urx, ury)
        #
        self.m_parent = parent
        self.m_children = {}
        #
        self.m_cell = None

    def set_hier_level(self, hier_level):
        self.m_hier_level = hier_level

    def get_hier_level(self):
        return self.m_hier_level

    def set_name(self, name):
        self.m_name = name

    def get_name(self):
        return self.m_name

    def set_current_A(self, current_A):
        self.m_current_A = current_A

    def get_current_A(self):
        return self.m_current_A

    def set_parent(self, parent):
        self.m_parent = parent

    def get_parent(self):
        return self.m_parent

    def add_child(self, child):
        self.m_children[child.m_name] = child

    def get_child(self, child_name):
        if child_name in self.m_children:
            return self.m_children[child_name]
        else:
            return None

    def get_children(self):
        return self.m_children

    def set_box(self, box):
        self.m_box = box

    def get_box(self):
        return self.m_box

    def update(self, box):
        self.m_box.update(box)

    def set_cell(self, cell):
        self.m_cell = cell

    def get_cell(self):
        return self.m_cell


class Cell:
    def __init__(self, name=""):
        self.m_name = name
        self.m_count = 0

    def set_name(self, name):
        self.m_name = name

    def get_name(self):
        return self.m_name

    def set_count(self, count):
        self.m_count = count

    def get_count(self):
        return self.m_count

    def increase_count(self, count=1):
        self.m_count += count


class MakeRCA:
    def __init__(self):
        pass

    def run(self, args):
        pass


def main(args):
    my_make_rca = MakeRCA()
    my_make_rca.run()


if __name__ == "__main__":
    main(sys.argv)
