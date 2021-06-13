import numpy as np
from .graph_generators import er_digraph_dale, reciprocitize
from .avalanche import network_avalanche_size


def parameter_scan_2par(nb_nodes, mesh1, mesh2, tstep=20):
    results = np.zeros((len(mesh1), len(mesh2), nb_nodes))
    for j, p_edge in enumerate(mesh1):
        for k, p_exc in enumerate(mesh2):
            print('{:d} {:d}'.format(j, k))
            ava_size_list = run_network_avalanche_size(nb_nodes, p_edge, p_exc, p_reci)
            results[j, k, :] = ava_size_list
    return results

def parameter_scan(par_list, mesh_list, fixed_par, nb_nodes, tstep=20):
    mesh1 = mesh_list[0]
    mesh2 = mesh_list[1]
    results = np.zeros((len(mesh1), len(mesh2), nb_nodes))
    for j, p1 in enumerate(mesh1):
        for k, p2 in enumerate(mesh2):
            print('{:d} {:d}'.format(j, k))
            par_dict = {par_list[0]: p1, par_list[1]: p2}
            par_dict = {**fixed_par, **par_dict,
                        'tstep':tstep, 'nb_nodes':nb_nodes}
            ava_size_list = run_network_avalanche_size(**par_dict)
            results[j, k, :] = ava_size_list
    return results

def run_network_avalanche_size(nb_nodes=10, p_edge=0.1, p_exc=0.5,
                               p_reci=0, tstep=20):
    if p_reci < 0 or p_reci > 1:
        raise ValueError('p_reci should be between 0 and 1!')
    graph = er_digraph_dale(nb_nodes, p_edge, p_exc)
    if p_reci > 0:
        graph = reciprocitize(graph, p_reci)
    ava_size_list = network_avalanche_size(graph, tstep=tstep)
    return ava_size_list
