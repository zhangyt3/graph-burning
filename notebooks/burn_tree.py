import networkx as nx
import operator


def shortest_path_lengths(graph):
    '''Returns a dictionary of dictionaries. dict[i][j] contains the distance
    between vertices i and j.'''
    dist_gen = nx.shortest_path_length(graph)

    node_distances = {}
    for node, distance_dict in dist_gen:
        node_distances[node] = distance_dict
        
    return node_distances


def find_farthest(node_distances, marked, root):
    '''Find the unmarked vertex farthest from the root (assumes root is  vertex 0)'''
    farthest = None
    for node, dist in node_distances[root].items():
        if node not in marked and (farthest is None or dist > node_distances[root][farthest]):
            farthest = node
    return farthest


def get_i_ancestor(node_distances, source, root, i):
    '''Return the ith ancestor of the source node.
    In a tree, the ith ancestor of any node is the node that is at distance
    i from it and is closer to the root.'''
    if i == 0:
        return source
    
    for node, dist in node_distances[source].items():
        if dist == i and node_distances[root][node] == node_distances[root][source] - i:
            return node
        
    raise RuntimeError("No ancestor found")
    

def burn_tree(tree, root=0):
    '''Implementation for tree burning algorithm (arbitrary root)
    Input:  a tree to burn
    Output: a burning sequence for the tree
    '''
    centers = []
    num_marked = []
    marked = set()
    
    # Calculate distance between all pairs of nodes
    node_distances = shortest_path_lengths(tree)
    
    i = 0
    while len(marked) < tree.order():
        # Find the unmarked vertex farthest from the root
        farthest = find_farthest(node_distances, marked, root)
        
        if node_distances[root][farthest] >= i:
            # Add the ith ancestor of the farthest node to centers
            i_ancestor = get_i_ancestor(node_distances, farthest, root, i)
            centers.insert(root, i_ancestor)
        elif root not in centers:
            # If there is no ith ancestor, add the root
            i_ancestor = root
            centers.insert(0, root)
        
        # Add all vertices within distance i of the i_ancestor to marked
        marked_it = 0
        for node in tree:
            if node_distances[i_ancestor][node] <= i:
                if node not in marked:
                    marked_it += 1
                    marked.add(node)
        
        num_marked.append(marked_it)
        
        i += 1
    
    return centers, num_marked


def get_central_node(eccentricities, marked):
    '''Return an umarked node of minimum eccentricity.'''
    cnode = None
    min_eccen = 34324312432

    for node, eccen in eccentricities.items():
        if node not in marked:
            if cnode is None or eccen < min_eccen:
                cnode = node
                min_eccen = eccen

    return cnode


def get_eccentricities(node_distances, marked):
    '''Return a dictionary (vertex -> eccentricity) wrt only unmarked nodes.'''
    eccentricities = {}

    for i in range(len(node_distances)):
        if i not in marked:
            dist_list = []

            # We only want to calculate eccentricity based on unmarked nodes
            for j in range(len(node_distances[i])):
                if j not in marked:
                    dist_list.append(node_distances[i][j])

            _, eccen = max(enumerate(dist_list), key=operator.itemgetter(1))
            eccentricities[i] = eccen

    return eccentricities


def burn_tree_using_centers(tree, update_root=True):
    '''Implementation for tree burning algorithm. Optionally choose to update the root 
    each loop iteration to be a vertex of minimum eccentricity.

    Input:  a tree to burn
    Output: a burning sequence for the tree
    '''
    centers = []
    marked = set()

    # Calculate distance between all pairs of nodes
    node_distances = shortest_path_lengths(tree)

    i = 0
    root = 0
    while len(marked) < tree.order():
        if update_root:
            eccentricities = get_eccentricities(node_distances, marked)
            root = get_central_node(eccentricities, marked)

        # Find the unmarked vertex farthest from the root
        farthest = find_farthest(node_distances, marked, root)

        if node_distances[root][farthest] >= i:
            # Add the ith ancestor of the farthest node to centers
            i_ancestor = get_i_ancestor(node_distances, farthest, root, i)
            centers.insert(0, i_ancestor)
        elif root not in centers:
            # If there is no ith ancestor, add the root
            i_ancestor = root  # Update this so the marking of vertices works later
            centers.insert(0, root)
        
        # Add all vertices within distance i of the i_ancestor to marked
        for node in tree:
            if node_distances[i_ancestor][node] <= i:
                marked.add(node)
        
        i += 1
    
    return centers

def get_leaves(tree, root=None):
    '''Return a list containing the leaves of a tree.'''
    if tree.order() == 1:
        return [node for node, nodedata in tree.nodes.items()]
    
    degrees = nx.classes.function.degree(tree)
    leaves = []

    for node, deg in degrees:
        if deg == 1 and node != root:
            leaves.append(node)
    
    return leaves


def get_neighbourhood(tree, source, radius, node_distances=None):
    '''Return all vertices within radius of the source vertex.'''
    if node_distances == None:
        node_distances = shortest_path_lengths(tree)
       
    neighbourhood = set()
    for node, dist in node_distances[source].items():
        if dist <= radius:
            neighbourhood.add(node)
    
    return neighbourhood


def is_burning_sequence(tree, sequence):
    '''Returns True if the sequence is a valid burning sequence.'''
    pass