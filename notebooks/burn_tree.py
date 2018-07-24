import networkx as nx
import operator
import math


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


def is_bridge(tree, node):
    '''Returns True if removing the given node will disconnect the tree.'''
    if not nx.algorithms.tree.recognition.is_tree(tree):
        raise nx.algorithms.tree.coding.NotATree()
    
    if nx.classes.function.degree(tree, node) <= 1:
        return False
    
    return True


def remove_nhood(tree, nhood):
    '''Removes as many nodes as possible from the tree while keeping the tree connected.'''
    tree = tree.copy()
    temp_hood = set()
    while True:
        changed = False
        eccens = nx.algorithms.distance_measures.eccentricity(tree)

        for node in nhood:               
            if not is_bridge(tree, node):
                tree.remove_node(node)
                changed = True
            else:
                temp_hood.add(node)

        nhood = temp_hood # So that we don't try to remove nodes that don't exist anymore
        temp_hood = set()

        # Exit loop when we cannot remove any more nodes
        if not changed or tree.order() == 0:
            break
            
    return tree
    

def burn_most_leaves_reroot(tree, verbose=False):
    '''Each iteration, root at a vertex of minimum eccentricity. Burns the vertex of height
    i whose neighbourhood contains the most leaves.'''
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


def burn_most_leaves_fixed_root(tree, verbose=False):
    '''Fix to root at the start to be a central vertex. Choose the vertex to burn based on 
    the number of leaves covered. If no vertices farther than sqrt(n) distance from the root,
    just burn the root.'''
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
                
        # TODO: move this check the start of the loop to fix bug
        # If no nodes far enough from the root, just burn the root
        if len(near_leaves2) == 0:
            # Pad the burning sequence to make it valid-ish
            num_to_fill = bound - len(activators) - 1 
            activators = [root] + ['x' for i in range(num_to_fill)] + activators
            break
        
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


def burn_most_removed(tree, verbose=False):
    '''Root at a central vertex each iteration. Choose the node to burn based on whose neighbourhood
    covers the most vertices that can be removed, without disconnecting the tree.'''
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
        
        # Remove any marked vertices that are now removeable
        for node in marked:
            if node in tree and not is_bridge(tree, node):
                tree.remove_node(node)
        
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
        
        # Mark all vertices in the neighbourhood that could not be removed
        for node in max_nhood:
            if node in tree:
                marked.add(node)
        
        i += 1
    
    return activators



