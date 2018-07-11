import unittest

import networkx as nx
from burn_tree import *


class TestBurningMethods(unittest.TestCase):
    
    def test_get_leaves(self):
        # Empty tree - return empty list
        tree = nx.Graph()
        leaves = get_leaves(tree)
        self.assertEqual(leaves, [])
        
        # Tree with 2 leaves
        edge_list = [(0, 1), (0, 2)]
        tree.add_edges_from(edge_list)
        leaves = get_leaves(tree)
        self.assertEqual(leaves, [1, 2])
        
        # Add some more edges
        more_edges = [(1, 3), (1, 4), (1, 5)]
        tree.add_edges_from(more_edges)
        leaves = get_leaves(tree)
        self.assertEqual(leaves, [2, 3, 4, 5])
        
        

if __name__ == '__main__':
    unittest.main()