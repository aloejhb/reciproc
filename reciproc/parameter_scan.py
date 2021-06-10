import numpy as np
from .graph_generators import er_digraph_dale
from .avalanche import network_avalanche_size


def parameter_scan(nb_nodes, mesh1, mesh2, tstep=20):
    results = np.zeros((len(mesh1), len(mesh2), nb_nodes))
    for j, p in enumerate(mesh1):
        for k, p_exc in enumerate(mesh2):
            print('{:d} {:d}'.format(j, k))
            graph = er_digraph_dale(nb_nodes, p, p_exc)
            ava_size_list = network_avalanche_size(graph, tstep=tstep)
            results[j, k, :] = ava_size_list
    return results
