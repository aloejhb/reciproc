import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from networkx.utils.decorators import py_random_state


def threshold_network(r0, W, thresh, tstep):
    if W.shape[0] != W.shape[1] or W.shape[0] != r0.shape[0]:
        raise Exception('W should be a square matrix with row number same as length of r0!')
    r = np.empty((r0.shape[0], tstep))
    r[:, 0] = r0
    for t in range(tstep-1):
        r[:, t+1] = np.matmul(W, r[:, t]) > thresh
    return r


def show_movie(movie):
    fig, ax = plt.subplots()
    ims = []
    for i in range(movie.shape[2]):
        im = plt.imshow(movie[:, :, i], animated=True)
        ims.append([im])
    ani = animation.ArtistAnimation(fig, ims, interval=50, repeat_delay=1000)
    plt.close(fig)
    return ani

@py_random_state(3)
def ei_network(graph, r0, tstep, seed=None):
    r = np.empty((r0.shape[0], tstep))
    r[:, 0] = r0
    for t in range(tstep-1):
        temp_graph = nx.create_empty_copy(graph)
        active_idx = np.nonzero(r[:,t])
        downstream_list = []
        for n in active_idx:
            for v1, v2, d in graph.out_edges(n, data=True):
                if seed.random() < d['weight']:
                    w = 1 * d['sign']
                else:
                    w = 0
                temp_graph.add_edge(v1, v2, weight=w)
                downstream_list.append(v2)
        downstream_list = set(downstream_list)
        for m in downstream_list:
            edata = temp_graph.in_edges(m, data=True)
            w_list = [d['weight'] for u, v, d in edata]
            w_list.append(0)
            r[m, t+1] = sum(w_list) > 0
    return r
