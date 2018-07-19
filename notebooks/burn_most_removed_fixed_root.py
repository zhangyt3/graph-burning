import networkx as nx
import math
from random import randint

from burn_tree import *


def burn_most_removed(tree, verbose=False):
    tree = tree.copy()
    
    activators = []
    marked = set()
    bound = math.ceil(math.sqrt(tree.order()))
    
    i = 0
    while tree.order() > 0:
        if verbose:
            print("\nTree size", tree.order())
            print("Nodes:", tree.nodes())
            print("Edges:", tree.edges())
        
        # First, root at a central vertex (min eccentricity)
        eccens = nx.algorithms.distance_measures.eccentricity(tree)
        root = min(eccens, key=eccens.get)
        
        # Consider all vertices v of height at most i - which N_i[v] covers the most leaves?
        leaves = get_leaves(tree, root=root)
        node_distances = shortest_path_lengths(tree)
        
        # Get all vertices within distance i of a leaf
        near_leaves = set()
        for leaf in leaves:
            nhood = get_neighbourhood(tree, source=leaf, radius=i, node_distances=node_distances)
            for node in nhood:
                near_leaves.add(node)
        
        # Remove those that are not >= sqrt(n) dist from the root
        near_leaves2 = set()
        for node in near_leaves:
            try:
                if node_distances[root][node] >= bound:
                    near_leaves2.add(node)
            except KeyError:
                print('\nNodes:', tree.nodes())
                print("root:", root)
                print("node:", node)
                
        # If no nodes far enough from the root, just burn the root
        if len(near_leaves2) == 0:
            # Pad the burning sequence to make it valid-ish
            num_to_fill = bound - len(activators) - 1 
            activators = [root] + ['x' for i in range(num_to_fill)] + activators
            break
        
        # From all these vertices, we will burn the one which covers most removable vertices
        max_node = None
        max_nhood = None
        max_removed = 0
        for node in near_leaves2:
            nhood = get_neighbourhood(tree, source=node, radius=i, node_distances=node_distances)
            tree_nhood_removed = remove_nhood(tree, nhood)
            num_removed = tree.order() - tree_nhood_removed.order()
            
            if num_removed > max_removed:
                max_node = node
                max_nhood = nhood
                max_removed = num_removed
            
        # Burn that vertex
        if max_node in activators:
            activators = [i if i != max_node else 'x' for i in activators]
        activators.insert(0, max_node)
        
        tree = remove_nhood(tree, max_nhood)
        
        i += 1
    
    return activators


if __name__ == '__main__':
    n = 2
    while True:   
        print("Order:", n, flush=True)

        trees = nx.generators.nonisomorphic_trees(n)
        for tree in trees:
            burning_sequence = burn_most_removed(tree)
            upper_bound = math.ceil(math.sqrt(tree.order()))

            if len(burning_sequence) > upper_bound:
                print('n={0:2d} | b(G)<={1:2d} | ceil(sqrt(n))={2:2d}'.format(tree.order(),
                                                                              len(burning_sequence),                  
                                                                              math.ceil(math.sqrt(tree.order()))), flush=True)
        n += 1
    