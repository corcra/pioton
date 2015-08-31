#!/bin/python
# Given two sets of points, visualise their displacements.

import numpy as np
#import matplotlib as mpl
#mpl.use('Agg')
import matplotlib.pyplot as plt

import src.vis as vis

def affine_transformation(d, trans=None):
    """
    Generate a random affine transformation using an augmented matrix.
    (using uniform random values)
        if trans is:
            True, the transformation is only a translation
            False, the transformation has no translation
            None, the transformation is fully affine
    """
    T = np.random.random(size=(d+1, d+1))
    T[-1, -1] = 1
    T[-1, :-1] = 0
    if not trans is None:
        if trans:
            T[:-1, :-1] = np.eye(d)
        else:
            T[:, -1] = 0
            T[-1, -1] = 1
    return T

def apply_transformation(A, T):
    """
    Does what it says on the tin.
    Since the transformation is using an augmented matrix, A is augmented here.
    Returns non-augmented B.
    """
    d = A.shape[1]
    assert T.shape[1] == d+1
    A_aug = np.ones(shape=(A.shape[0], d+1))
    A_aug[:, :-1] = A
    B_aug = np.einsum('kj,ij', T, A_aug)
    B = B_aug[:, :-1]
    assert B.shape == A.shape
    return B

def roll(trans_opt=None):
    """
    Run the whole procedure.
    """
    d = 2
    n_samples = 10
    A = np.random.normal(size=(n_samples, d))
    T = affine_transformation(d, trans=trans_opt)
    print T
    print np.linalg.det(T)
    B = apply_transformation(A, T)
    vis.plot_displacement(A, B)
