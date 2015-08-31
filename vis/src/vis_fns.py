#!/bin/python
# Given two sets of points, visualise their displacements.

import numpy as np
#import matplotlib as mpl
#mpl.use('Agg')
import matplotlib.pyplot as plt

def plot_displacement(A, B, save=False):
    """
    A and B are both num_samples x num_dimensions
    for now, num_dimensions must = 2
    """
    assert A.shape == B.shape
    assert A.shape[1] == 2
    delta = B - A
    delta_dir = delta/np.linalg.norm(delta, axis=1).reshape(-1, 1)
    fig = plt.figure()
    # set size
    xmin = min(min(A[:, 0]), min(B[:, 0]))
    xmax = max(max(A[:, 0]), max(B[:, 0]))
    ymin = min(min(A[:, 1]), min(B[:, 1]))
    ymax = max(max(A[:, 1]), max(B[:, 1]))
    plt.xlim(1.1*xmin, 1.1*xmax)
    plt.ylim(1.1*ymin, 1.1*ymax)
    # create
    # add displacement arrows
    offset = 0.05
    for i in xrange(A.shape[0]):
        plt.arrow(A[i, 0]+offset*delta_dir[i, 0], A[i, 1]+offset*delta_dir[i, 1],
                  delta[i, 0]-2*offset*delta_dir[i, 0], delta[i, 1]-2*offset*delta_dir[i, 1],
                  length_includes_head=True, alpha=0.5, color='grey',
                  head_width=0.08, head_length=0.08, width=0.009)
    plt.scatter(A[:, 0], A[:, 1], s=35, c='red', linewidths=0)
    plt.scatter(B[:, 0], B[:, 1], s=35, c='blue', linewidths=0)
    # show
    if save:
        plt.savefig('fig.png')
    else:
        plt.show()
    return True
