import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation



def threshold_network(r0,W,thresh,tstep):
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
