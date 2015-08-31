#!/bin/python
# Given two sets of points, visualise their displacements.

import numpy as np
#import matplotlib as mpl
#mpl.use('Agg')
import matplotlib.pyplot as plt
import math

import src.vis as vis

def rotation(d=2, theta=None):
    """
    Generate (random) rotation matrix.
    (using augmented matrix, because T is expected in this format)
    """
    assert d == 2
    print 'Generating rotation with angle', math.degrees(theta), 'degrees'
    if theta is None:
        theta = np.random.random()*2*math.pi        # in radians
    T = np.eye(3)
    T[0, 0] = math.cos(theta)
    T[0, 1] = -math.sin(theta)
    T[1, 0] = math.sin(theta)
    T[1, 1] = math.cos(theta)
    return T

def affine_transformation(d=2, trans=None, preserve_area=False):
    """
    Generate a random affine transformation using an augmented matrix.
    (using uniform random values)
        if trans is:
            True, the transformation is only a translation
            False, the transformation has no translation
            None, the transformation is fully affine
        if preserve_area is:
            True, the absolute value of the determinant is 1
    """
    T = np.random.normal(size=(d+1, d+1))
    T[-1, -1] = 1
    T[-1, :-1] = 0
    if not trans is None:
        if trans:
            print 'Generating translation.'
            T[:-1, :-1] = np.eye(d)
        else:
            print 'Generating linear transformation.'
            T[:, -1] = 0
            T[-1, -1] = 1
    else:
        print 'Generating affine transformation.'
    if preserve_area:
        print 'Rescaling to ensure abs(det) = 1 for transformation component.'
        # (note, this actually ensures abs(det) == 1 for the entire matrix)
        sub_det = np.linalg.det(T[:-1,:-1])
        c = pow((1.0/abs(sub_det)), 1.0/d)
        T[:-1,:-1] *= c
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

def roll(A=None, T=None, trans=None):
    """
    Run the whole procedure.
    """
    d = 2
    if A is None:
        n_samples = 10
        A = np.random.normal(size=(n_samples, d))
    if T is None:
        T = affine_transformation(d, trans=trans)
    print T
    print 'determinant:', np.linalg.det(T)
    B = apply_transformation(A, T)
    vis.plot_displacement(A, B)
