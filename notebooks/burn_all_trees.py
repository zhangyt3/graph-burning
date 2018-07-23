import networkx as nx
import math
from random import randint
import argparse

from burn_tree import *


parser = argparse.ArgumentParser(description='Process which burning algorithm to use')
parser.add_argument('--alg',
                    type=str,
                    help='the algorithm to use (frl, rrl, rrr, md)',
                    required=True)


if __name__ == '__main__':
    args = parser.parse_args()
    alg = args.alg
    
    print("Using algorithm", alg)
    
    n = 2
    while True:   
        print("\n" + "*"*20)
        print("Order:", n, flush=True)
        print("*"*20)
        
        # Burn all non-isomorphic trees of order n
        trees = nx.generators.nonisomorphic_trees(n)
        num_trees = 0
        for tree in trees:
            upper_bound = math.ceil(math.sqrt(tree.order()))
            
            if alg == 'frl':
                # Fixed Root, Most Leaves
                burning_sequence = burn_most_leaves_fixed_root(tree)
            elif alg == 'rrl':
                # Re-Root, Most Leaves
                burning_sequence = burn_most_leaves_reroot(tree)
            elif alg == 'md':
                # Max Depth
                burning_sequence, marked = burn_tree(tree)
            else:
                # Re-Root, Most Removable Nodes
                burning_sequence = burn_most_removed(tree)
    
            if len(burning_sequence) > upper_bound:
                print('n={0:2d} | b(G)<={1:2d} | ceil(sqrt(n))={2:2d}'.format(tree.order(),
                                                                              len(burning_sequence),                  
                                                                              math.ceil(math.sqrt(tree.order()))), flush=True)
                print("Nodes:", tree.nodes())
                print("Edges:", tree.edges())
                print()
                
            num_trees += 1
        
        print(tree)
        print("There are {} trees of order {}".format(num_trees, n))
        n += 1
    