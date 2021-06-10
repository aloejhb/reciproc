import numpy as np
import networkx as nx
from .threshold_network import threshold_network
def avalanche_size(r):
    """
    Returns avalanche size from simulated activity of a network
    Parameters
    ----------
    r: np.array (N*tstep)
       Simulation result for all neurons in each time step
    """
    active_flag = np.max(r, axis=1) > 0
    return sum(active_flag)

def network_avalanche_size(graph, tstep=30):
    thresh = 0
    W = nx.to_numpy_matrix(graph)
    N = graph.number_of_nodes()
    ava_size_list = np.zeros(N)
    for index in range(N):
        r0 = np.zeros(N)
        r0[index] = 1.0
        r = threshold_network(r0, W, thresh, tstep)
        ava_size = avalanche_size(r)
        ava_size_list[index] = ava_size
    return ava_size_list
