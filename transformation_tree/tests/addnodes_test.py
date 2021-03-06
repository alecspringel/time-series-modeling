"""
Tree tests: testing add_nodes_** methods

USE: 'pytest' in command line to execute
"""
import pytest
import os
import sys
from .testops import op1, op2, op3, root
# Needed to import from parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# IGNORE IMPORT NOT AT TOP OF FILE
from tree import TTree, Node


# TESTS
def test_add_nodes():
    tree = TTree("test", Node(root))
    nodes = [Node(op1), Node(op2), Node(op3)]
    tree.add_nodes(tree.root, nodes)
    print(tree)
    # Check if each node in tree has 1 child and all nodes were added to tree
    assert len(tree.root.children) == 3


def test_add_nodes_byid():
    tree = TTree("test", Node(root))
    nodes = [Node(op1), Node(op2), Node(op3)]
    tree.add_nodes_byid(0, nodes)
    print(tree)
    # Check if each node in tree has 1 child and all nodes were added to tree
    assert len(tree.root.children) == 3
