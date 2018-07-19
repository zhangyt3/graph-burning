import networkx as nx
import math
from random import randint

from burn_tree import *


def burn_most_leaves_rooted2(tree, verbose=False):
    tree = tree.copy()
    
    activators = []
    marked = set()
    bound = math.ceil(math.sqrt(tree.order()))
    
    # First, root at a central vertex (min eccentricity)
    eccens = nx.algorithms.distance_measures.eccentricity(tree)
    root = min(eccens, key=eccens.get)
    
    i = 0
    while tree.order() > 0:
        if verbose:
            print("\nTree size", tree.order())
            print("Nodes:", tree.nodes())
            print("Edges:", tree.edges())
        
        # Calculate a new root each iteration
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
                
        # If no nodes far enough from the root, consider all nodes
        if len(near_leaves2) == 0:
            near_leaves2 = near_leaves
        
        # For all v we just got: take one with max leaves in its neighbourhood
        max_leaves = 0
        max_node = None
        max_nhood = None
        max_removed = 0
        for node in near_leaves2:
            nhood = get_neighbourhood(tree, source=node, radius=i, node_distances=node_distances)
            
            num_leaves = 0
            for v in nhood:
                if v in leaves:
                    num_leaves += 1

            if num_leaves > max_leaves:
                max_node = node
                max_nhood = nhood
                max_leaves = num_leaves
                
                tree_nhood_removed = remove_nhood(tree, nhood)
                max_removed = tree.order() - tree_nhood_removed.order()
                
            elif num_leaves == max_leaves:
                tree_nhood_removed = remove_nhood(tree, nhood)
                num_removed = tree.order() - tree_nhood_removed.order()
                
                if num_removed > max_removed:
                    max_node = node
                    max_nhood = nhood
                    max_leaves = num_leaves
                    max_removed = num_removed
            
        # Burn that vertex
        if max_node in activators:
            activators.remove(max_node)
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
            burning_sequence = burn_most_leaves_rooted2(tree)
            upper_bound = math.ceil(math.sqrt(tree.order()))

            if len(burning_sequence) > upper_bound:
                print('n={0:2d} | b(G)<={1:2d} | ceil(sqrt(n))={2:2d}'.format(tree.order(),
                                                                              len(burning_sequence),                  
                                                                              math.ceil(math.sqrt(tree.order()))), flush=True)
        n += 1
    
    
    