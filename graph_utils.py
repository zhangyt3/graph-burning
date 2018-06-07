from pprint import pprint
import numpy as np

def create_adj_mat(filepath):
    '''Given a filepath, reads the contents and returns an adjacency matrix.'''
    adj_mat = []
    with open(filepath, 'r') as file:
        # Read all lines from the file...
        lines = [line.strip() for line in file]

        for line in lines:
            if len(line) > 0:
                adj_mat.append([int(x) for x in line.split(' ')])
    
    return np.array(adj_mat)


if __name__ == '__main__':
    pprint(create_adj_mat('./trees/cross.mat'))
    pprint(create_adj_mat('./trees/ethane.mat'))    

        