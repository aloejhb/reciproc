import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from networkx.utils.decorators import py_random_state

def er_digraph(n, p):
    G = nx.gnp_random_graph(n, p, seed=None, directed=True)
    return G

# @py_random_state(2)
def assign_cell_type(G, p):
    """
    Returns a graph with inhibitory and excitatory cells.
    Parameters
    ----------
    G : nx.DiGraph
        The directed graph
    p : float
        Probability for each cell to be excitatory.
    """
    ct_list = np.random.choice([-1, 1], size=G.number_of_nodes(), p=[1-p, p])
    keys = list(G.nodes)
    cell_type = dict(zip(keys, ct_list))
    nx.set_node_attributes(G, cell_type, 'cell_type')
    for u, v, d in G.out_edges(data=True):
        if G.nodes[u]['cell_type'] == 1:
            d['sign'] = 1
        else:
            d['sign'] = -1
    return G


def assign_weight(G):
    for u, v, d in G.out_edges(data=True):
        d['weight'] = np.random.random()
    return G


def er_digraph_dale(n, p, p_exc):
    G = er_digraph(n, p)
    G = assign_weight(G)
    G = assign_cell_type(G, p_exc)
    return G


def assign_edge_type_binomial(G, p):
    pass


@py_random_state(2)
def reciprocitize(G, p, seed=None):
    """
    Add opposite edge if it does not exists
    with probability p
    """
    if p < 0 or p > 1:
        raise ValueError('p_reci should be between 0 and 1!')

    G_copy = G.copy()
    for u, v in G_copy.out_edges():
        if not G_copy.has_edge(v, u):
            if seed.random() < p:
                G_copy.add_edge(v, u, weight=G_copy.nodes[v]['cell_type'])
    return G_copy










def draw_weighted_graph(G):
    eexc = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] > 0]
    einh= [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] <= 0]

    pos = nx.spring_layout(G)  # positions for all nodes

    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=20)

    # edges
    nx.draw_networkx_edges(G, pos, edgelist=eexc, edge_color='r', alpha=0.5)
    nx.draw_networkx_edges(G, pos, edgelist=einh, edge_color='b', alpha=0.2)


def plot_eigenvalue_spectra(lam):
    plt.figure(figsize=(5, 10))
    plt.subplot(2, 1, 1)
    xx = plt.hist(np.real(lam), bins=50)
    plt.subplot(2, 1, 2)
    plot_complex_scatter(lam)


def plot_complex_scatter(z, **kwargs):
    X = [x.real for x in z]
    Y = [x.imag for x in z]
    plt.scatter(X, Y, **kwargs)
