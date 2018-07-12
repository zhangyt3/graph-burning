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
    
    def test_get_neighbourhood_p2(self):
        # Path on two nodes: 0-1
        tree = nx.Graph()
        tree.add_edge(0, 1)
        
        nhood = get_neighbourhood(tree, source=0, radius=1)
        self.assertEqual(nhood, set([0, 1]))
        
        nhood = get_neighbourhood(tree, source=1, radius=1)
        self.assertEqual(nhood, set([0, 1]))
        
    def test_get_neighbourhood_p3(self):
        # Path on three nodes: 0-1-2
        tree = nx.Graph()
        tree.add_edge(0, 1)
        tree.add_edge(1, 2)
        
        nhood = get_neighbourhood(tree, source=1, radius=0)
        self.assertEqual(nhood, set([1]))
        
        nhood = get_neighbourhood(tree, source=1, radius=1)
        self.assertEqual(nhood, set([0, 1, 2]))
        
        nhood = get_neighbourhood(tree, source=1, radius=2)
        self.assertEqual(nhood, set([0, 1, 2]))
        
        nhood = get_neighbourhood(tree, source=2, radius=2)
        self.assertEqual(nhood, set([0, 1, 2]))
        
        nhood = get_neighbourhood(tree, source=2, radius=1)
        self.assertEqual(nhood, set([1, 2]))
    
    def test_get_neighbourhood_star(self):
        # Vertex 0 is connected to all other vertices, all other vertices are leaves
        tree = nx.Graph()
        edge_list = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5)]
        tree.add_edges_from(edge_list)
        
        nhood = get_neighbourhood(tree, source=0, radius=0)
        self.assertEqual(nhood, set([0]))
        
        nhood = get_neighbourhood(tree, source=0, radius=1)
        self.assertEqual(nhood, set([0, 1, 2, 3, 4, 5]))
        
        for node in range(1, 6):
            nhood = get_neighbourhood(tree, source=node, radius=1)
            self.assertEqual(nhood, set([0, node]))
            

if __name__ == '__main__':
    unittest.main()