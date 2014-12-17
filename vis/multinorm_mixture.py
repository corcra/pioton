#!/bin/python
# Roughly this is about visualising a probability distribution over a 2D space.
# It's not random.
# The PDF is given by a mixture of 2D gaussians with:
# (for each component of the mixture)
# a uniform prior (between -1 and +1) over means
# a uniform prior over the *scale* of the covariance matrix, given a randomly-generated one.

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.stats import multivariate_normal
import sys

if len(sys.argv) < 3:
    N = 1000
    centres = N/50
    print 'Using defaults: \nN =', N, '\ncentres =', centres
else:
    N = int(sys.argv[1])
    centres = int(sys.argv[2])
# make the mesh
X = np.linspace(-1, 1, N)
Y = np.linspace(-1, 1, N)
X, Y = np.meshgrid(X, Y)
# this nonsense is for scipy's multivariate_normal
pos = np.empty(X.shape + (2,))
pos[:, :, 0] = X
pos[:, :, 1] = Y
# generate a positive semidefinite matrix
# (yep, same one for all components right now)
A = np.random.rand(2,2)
cov = np.dot(A,A.T)
print 'Covariance matrix:'
print cov
# build mixture components
pi = np.random.rand(centres)
pi = pi/np.sum(pi)
# sequentially build Z up
Z = 0
for n in xrange(centres):
    mean = 1 - 2*np.random.rand(2)
    scale = np.random.rand(1)
    Z = Z + pi[n]*multivariate_normal.pdf(pos, mean, scale*cov)
# normalise
Z = Z/np.sum(Z)

plt.clf()
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='cool', linewidth=0)
plt.savefig('3D.png')
plt.close()
