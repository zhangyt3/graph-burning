import networkx as nx


def shortest_path_lengths(graph):
    '''Returns a dictionary of dictionaries. dict[i][j] contains the distance
    between vertices i and j.'''
    dist_gen = nx.shortest_path_length(graph)

    node_distances = {}
    for node, distance_dict in dist_gen:
        node_distances[node] = distance_dict
        
    return node_distances


def find_farthest(node_distances, marked):
    '''Find the unmarked vertex farthest from the root (assumes root is  vertex 0)'''
    farthest = None
    for node, dist in node_distances[0].items():
        if node not in marked and (farthest is None or dist > node_distances[0][farthest]):
            farthest = node
    return farthest


def get_i_ancestor(node_distances, source, i):
    '''Return the ith ancestor of the source node.
    In a tree, the ith ancestor of any node is the node that is at distance
    i from it and is closer to the root.'''
    if i == 0:
        return source
    
    for node, dist in node_distances[source].items():
        if dist == i and node_distances[0][node] == node_distances[0][source] - i:
            return node
        
    raise RuntimeError("No ancestor found")
    

def burn_tree(tree):
    '''Implementation for tree burning algorithm (arbitrary root)
    Input:  a tree to burn
    Output: a burning sequence for the tree
    '''
    centers = []
    marked = set()
    
    # Calculate distance between all pairs of nodes
    node_distances = shortest_path_lengths(tree)
    
    i = 0
    while len(marked) < tree.order():
        # Find the unmarked vertex farthest from the root (assumes root is  vertex 0)
        farthest = find_farthest(node_distances, marked)
        
        if node_distances[0][farthest] >= i:
            # Add the ith ancestor of the farthest node to centers
            i_ancestor = get_i_ancestor(node_distances, farthest, i)
            centers.insert(0, i_ancestor)
        elif 0 not in centers:
            # If there is no ith ancestor, add the root
            centers.insert(0, 0)
        
        # Add all vertices within distance i of the i_ancestor to marked
        for node in tree:
            if node_distances[i_ancestor][node] <= i:
                marked.add(node)
        
        i += 1
    
    return centers

def burn_tree_using_centers(tree):
    '''Implementation for tree burning algorithm (root at center each iteration)'''
    pass


def is_burning_sequence(tree, sequence):
    '''Returns True if the sequence is a valid burning sequence.'''
    pass