import sys
import argparse
import copy
import numpy as np


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

    def get_y(self):
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
    def __init__(self, name="", box=Box(), current_A=0.0):
        self.m_name = name
        self.m_box = copy.deepcopy(box)
        self.m_current_A = current_A

    def set_name(self, name):
        self.m_name = name

    def get_name(self):
        return self.m_name

    def set_box(self, box):
        self.m_box = box

    def get_box(self):
        return self.m_box

    def set_current_A(self, current_A):
        self.m_current_A = current_A

    def get_current_A(self):
        return self.m_current_A

    def add_current_A(self, current_A):
        self.m_current_A += current_A


class Treenode:
    def __init__(self, instance=Instance(), level=-1, parent=None):
        self.m_instance = instance
        self.m_level = level
        self.m_parent = parent
        self.m_children = {}

    def set_instance(self, instance):
        self.m_instance = instance

    def get_instance(self):
        return self.m_instance

    def set_level(self, level):
        self.m_level = level

    def get_level(self):
        return self.m_level

    def set_parent(self, parent):
        self.m_parent = parent

    def get_parent(self):
        return self.m_parent

    def add_child(self, child):
        if not child.get_instance().get_name() in self.m_children:
            self.m_children[child.get_instance().get_name()] = child

    def get_children(self):
        return self.m_children

    def get_child(self, name):
        if name in self.m_children:
            return self.m_children[name]
        else:
            return None


class Tree:
    def __init__(self, root_treenode=Treenode()):
        self.m_root_treenode = root_treenode

    def set_root_treenode(self, root_treenode):
        self.m_root_treenode = root_treenode

    def get_root_treenode(self):
        return self.m_root_treenode

    def add_treenode(self, parent, level, names, current_A):
        if level >= len(names):
            return
        if 0 == level:
            parent.get_instance().add_current_A(current_A)
        #
        name = names[level]
        child = parent.get_child(name)
        if None == child:
            child = Treenode(Instance(name), level, parent)
            child.get_instance().set_current_A(current_A)
            parent.add_child(child)
        else:
            child.get_instance().add_current_A(current_A)
        #
        self.add_treenode(child, level + 1, names, current_A)

    def update_box(self, parent, level, names, box):
        if level >= len(names):
            return
        if 0 == level:
            parent.get_instance().get_box().update(box)
        #
        name = names[level]
        child = parent.get_child(name)
        if None != child:
            child.get_instance().get_box().update(box)
            self.update_box(child, level + 1, names, box)

    def print(self, parent, hier_path, level):
        if 0 == level:
            msg = f"+ 0 - root {parent.get_instance().get_current_A()} {parent.get_instance().get_current_A()} {parent.get_instance().get_box().get_str()}"
            print(f"{msg}")
        for child_name in parent.get_children():
            child = parent.get_children()[child_name]
            #
            msg = ""
            if "" == hier_path:
                msg = f"{self.print_hier_space(level)} {level} - {child.get_instance().get_name()} {child.get_instance().get_current_A()} {child.get_instance().get_box().get_str()}"
            else:
                msg = f"{self.print_hier_space(level)} {level} {hier_path} {child.get_instance().get_name()} {child.get_instance().get_current_A()} {child.get_instance().get_box().get_str()}"
            print(f"{msg}")
            #
            hier_path_1 = hier_path + str(".") + child_name
            if 0 == len(hier_path):
                hier_path_1 = child_name
            self.print(child, hier_path_1, level + 1)

    def print_hier_space(self, level):
        msg = "+"
        for i in range(0, level + 1):
            msg += "-"
        return msg

    def write_rca_file(
        self,
        parent,
        hier_path,
        level,
        layer_name,
        net_name,
        probe_distance,
        rca_file,
    ):
        if 0 == len(parent.get_children()):
            rca_file.write(
                f"{hier_path} {layer_name} {net_name} - {parent.get_instance().get_current_A()} {parent.get_instance().get_box().get_str()} {probe_distance}\n"
            )
        else:
            for child_name in parent.get_children():
                child = parent.get_children()[child_name]
                hier_path_1 = f"{hier_path}.{child_name}"
                if "" == hier_path:
                    hier_path_1 = child_name
                self.write_rca_file(
                    child,
                    hier_path_1,
                    level + 1,
                    layer_name,
                    net_name,
                    probe_distance,
                    rca_file,
                )


class MakeRCA:
    def __init__(self, tree=Tree()):
        self.m_version = "20250919.0.0"
        self.m_argparser = argparse.ArgumentParser()
        self.m_output_prefix = ""
        self.m_instance_bbox_file_name = ""
        self.m_instance_current_file_name = ""
        self.m_layer_name = ""
        self.m_net_name = ""
        self.m_level = np.iinfo(np.int32).max
        #
        self.m_total_current_A = 0.0
        #
        self.m_tree = copy.deepcopy(tree)

    def add_total_current_A(self, current_A):
        self.m_total_current_A += current_A

    def get_total_current_A(self):
        return self.m_total_current_A

    def read_args(self, args):
        print(f"# read args start")
        self.m_argparser.add_argument(
            "output_prefix", type=str, help="output prefix"
        )
        self.m_argparser.add_argument(
            "instance_bbox_file", type=str, help="instance bbox file"
        )
        self.m_argparser.add_argument(
            "instance_current_file", type=str, help="instance current file"
        )
        self.m_argparser.add_argument("layer", type=str, help="layer name")
        self.m_argparser.add_argument("net", type=str, help="net name")
        self.m_argparser.add_argument(
            "--level",
            type=int,
            default=np.iinfo(np.int32).max,
            help="hierarchical level(0~)",
        )
        #
        args = self.m_argparser.parse_args(args[1:])
        #
        self.m_output_prefix = args.output_prefix
        self.m_instance_bbox_file_name = args.instance_bbox_file
        self.m_instance_current_file_name = args.instance_current_file
        self.m_layer_name = args.layer
        self.m_net_name = args.net
        self.m_level = args.level
        #
        print(f"# read args end")

    def print_inputs(self):
        print(f"# print inputs start")
        print(f"output prefix           : {self.m_output_prefix}")
        print(f"instance bbox file      : {self.m_instance_bbox_file_name}")
        print(f"instance current file   : {self.m_instance_current_file_name}")
        print(f"layer                   : {self.m_layer_name}")
        print(f"net                     : {self.m_net_name}")
        print(f"level                   : {self.m_level}")
        print(f"# print inputs end")

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
            tokens = line1.split()
            if 2 != len(tokens):
                continue
            #
            instance_path = self.get_instance_path(tokens[0])
            instance_paths = instance_path.split(".")
            current_A = float(tokens[1])
            self.add_total_current_A(current_A)
            self.m_tree.add_treenode(
                self.m_tree.get_root_treenode(), 0, instance_paths, current_A
            )
        print(f"{nlines} lines")
        f.close()
        print(f"total current[A] : {self.m_total_current_A}")
        print(
            f"# read instance current file({self.m_instance_current_file_name}) start"
        )

    def get_instance_path(self, name):
        instance_path = name
        tokens = instance_path.split(".")
        if len(tokens) < self.m_level:
            return instance_path
        else:
            return ".".join(tokens[0 : self.m_level + 1])

    # cell_path
    #   instance_path (cx,cy) ((llx,lly) (urx,ury)
    def read_instance_bbox_file(self):
        print(
            f"# read instance bbox file({self.m_instance_bbox_file_name}) start"
        )
        nlines = 0
        f = open(self.m_instance_bbox_file_name, "rt")
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
            line1 = line1.replace("(", " ").replace(")", " ").replace(",", " ")
            if 0 == len(line1):
                continue
            #
            tokens = line1.split()
            if 7 != len(tokens):
                continue
            #
            name = tokens[0]
            instance_name = self.make_instance_name(name)
            instance_names = instance_name.split(".")
            #
            llx = float(tokens[3])
            lly = float(tokens[4])
            urx = float(tokens[5])
            ury = float(tokens[6])
            box = Box(llx, lly, urx, ury)
            #
            self.m_tree.update_box(
                self.m_tree.get_root_treenode(), 0, instance_names, box
            )
        print(f"{nlines} lines")
        f.close()
        print(
            f"# read instance bbox file({self.m_instance_bbox_file_name}) end"
        )

    def print_tree(self):
        print(f"# print tree start")
        self.m_tree.print(self.m_tree.get_root_treenode(), "", 0)
        print(f"# print tree end")

    def make_instance_name(self, name):
        tokens = name.split("/")
        for i in range(len(tokens)):
            tokens[i] = f"X{tokens[i]}"
        return ".".join(tokens)

    def write_rca_file(self):
        file_name = f"{self.m_output_prefix}.rca"
        print(f"# write rca file({file_name}) start")
        f = open(file_name, "wt")
        self.m_tree.write_rca_file(
            self.m_tree.get_root_treenode(),
            "",
            0,
            self.m_layer_name,
            self.m_net_name,
            0.5,
            f,
        )
        f.close()
        print(f"# write rca file({file_name}) end")

    def run(self, args):
        print(f"# make_rca.py({self.m_version}) start")
        self.read_args(args)
        self.print_inputs()
        self.read_instance_current_file()
        # self.print_tree()
        self.read_instance_bbox_file()
        self.print_tree()
        self.write_rca_file()
        print(f"# make_rca.py({self.m_version}) end")


def main(args):
    my_make_rca = MakeRCA()
    my_make_rca.run(args)


if __name__ == "__main__":
    main(sys.argv)
