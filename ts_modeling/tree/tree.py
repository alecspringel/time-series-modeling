"""
Utility: Tree backend for storing all potential pipelines.
Todo:
Transformation Tree object
    * Some class methods we should add:
        adding a list of nodes as children of target...
        > add_nodes (ref to node, [Node] or Node)
        > add_nodes_byname (target_name, [Node] or Node)
        > add_nodes_byid (target_id, [Node] or Node)

        > get_all_nodes_oftype(op_name) # this returns all operators of
          specified type as a list

        > reparent nodes in the tree
"""
from __future__ import annotations
from anytree import NodeMixin, RenderTree, render, PostOrderIter
from typing import List, Callable, Union
from tree_helpers import *
import pickle

__authors__ = "Alec Springel, Seth Tal"
__version__ = "1.0.0"
__emails__ = "aspring6@uoregon.edu, stal@uoregon.edu"
__credits__ = "Kyra Novitzky, Ronny Fuentes, Stephanie Schofield"
__date__ = "01/23/2021"


class Node(NodeMixin):
    def __init__(self, function: Callable, parent: Node = None,
                 children: [Node] = None):
        self.name = function.__name__
        self.function = function
        self.parent = parent
        self.id = None  # Private
        if children is not None:
            self.children = children

    def __repr__(self):
        """__repr__ allows us to define the default string representation
        of this class"""
        return 'Operator: {}'.format(self.name)

    def set_id(self, id):
        self.id = id

    def get_id(self):
        return self.id

    def set_parent(self, parent):
        self.parent = parent
        return self.parent

    def set_children(self, children):
        self.children = children

    def copy(self):
        return Node(self.function, self.parent, self.children)


class TTree():
    def __init__(self, name: str, root: Node):
        self.name = name
        self.root = root
        self.root.set_id(0)
        self.id_iterator = 1

        # self.__nodes is just a list containing references of every node in the tree
        # It is just a nice little helper attribute (ez way to check if nodes are
        # contained in the tree)
        self.__nodes = [root]

    def save(self, file: str):
        """Saves tree to as serialized object to specified file path"""
        with open(file, 'wb') as handle:
            pickle.dump(self, handle)

    def set_id(self, node: Node):
        """For use inside of the TTree() class only.
        Sets a node's IDs"""
        node.set_id(self.id_iterator)
        self.id_iterator += 1

    def print_tree(self, id=False):
        """Prints a visual representation of the tree"""
        for pre, fill, node in RenderTree(self.root):
            if(id):
                treestr = u"%s%s (%s)" % (pre, node.name, node.id)
            else:
                treestr = u"%s%s" % (pre, node.name)
            print(treestr.ljust(8))

    def print_nodes_as_list(self):
        print(self.__nodes)

    def add_node(self, target: Node, new_node: Node):
        # if either arg is not null
        if target and new_node:
            # if target is contained within the tree
            if target in self.__nodes:
                # set parent of new node
                new_node.set_parent(target)

                # add new node as child of target
                # if target.children:
                #     target.children.append(new_node)
                # else:
                #     target.children = [new_node]

                # update tree to contain new node
                self.__nodes.append(new_node)
                # Set the runtime ID of the new Node
                self.set_id(new_node)
        pass

    def add_nodes(self, target: Node, nodes: [Node]):
        pass

    def add_nodes_byname(self, operator: str, nodes: [Node]):
        pass

    def __add_newpath_byref(self, target: Node, path: [Node]):
        """PRIVATE: Helper function for adding paths by reference to
        target node"""
        path[0].set_parent(target)
        self.set_id(path[0])
        for i in range(1, len(path)):
            path[i].set_parent(path[i-1])
            self.set_id(path[i])

    def add_newpath(self, target: Node, path: Union[Node, [Node]]):
        """Builds a path starting with target node, and iterating through path,
        inserting these nodes as children of eachother
        (starting with target)"""
        if(type(path) is not list):  # Allows single node as parameter
            path = [path]
        for node in path:
            if node.id:
                # Throw error
                raise Exception("Nodes within new path cannot be "
                                "contained in the tree already.")
        self.__add_newpath_byref(target, path)

    # ! We need to come back to this
    # def add_newpath_byname(self, target_name: str, path: Union[Node, [Node]]):
    #     """Builds a path starting with target node, and iterating through path,
    #     inserting these nodes as children of eachother
    #     (starting with target)

    #     Note: User will lose references to original path (need to make copy)
    #     """
    #     if(type(path) is not list):  # Allows single node as parameter
    #         path = [path]
    #     targets = [node for node in PostOrderIter(self.root,
    #                                               filter_=lambda n:
    #                                               n.name == target_name)]
    #     for target in targets:
    #         # Need to make copy of path, otherwise anytree will move the path
    #         # to a new target on each iteration (bc the refs haven't changed)
    #         path_copy = copy_path(path)
    #         self.__add_newpath_byref(target, path_copy)

    def add_newpath_byid(self, target_id: int, path: Union[Node, [Node]]):
        if(type(path) is not list):  # Allows single node as parameter
            path = [path]
        # If any node in the new path is already contained in tree, throw error
        for node in path:
            if node.id:
                raise Exception(
                    "Nodes within new path cannot be contained in the tree already.")
        targets = [node for node in PostOrderIter(self.root,
                                                  filter_=lambda n:
                                                  n.id == target_id)]

        for target in targets:
            # Need to make copy of path, otherwise anytree will move the path
            # to a new target on each iteration (bc the refs haven't changed)
            self.__add_newpath_byref(target, path)


def load_tree(file: str) -> TTree:
    """Loads tree as python object from specified file path"""
    with open(file, 'rb') as handle:
        tree = pickle.load(handle)
    return tree
