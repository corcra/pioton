#!/bin/python
# Roughly this is about visualising a probability distribution over a 2D space.
# It's not random.
# The PDF is given by a mixture of 2D gaussians with:
# (for each component of the mixture)
# a uniform prior (between -1 and +1) over means
# a uniform prior over the *scale* of the covariance matrix, given a randomly-generated one.
#
# TODO
# 1. Prettify scale on Z-axis.
# 2. Experiment with other colour maps.
# 3. Put a better prior on the covariance matrices.
# 4. Better resolution/cropping on savefig.

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.stats import multivariate_normal
import sys

rescale = True
if rescale:
    # this is for forcing the unnormalised probabilities to fall between
    # exp(-1) and exp(1)
    good_min = np.exp(-1)
    good_max = np.exp(1)
    good_range = good_max - good_min

if len(sys.argv) < 3:
    N = 1000
    components = N/50
    print 'Using defaults: \nN =', N, '\ncomponents =', components
else:
    N = int(sys.argv[1])
    components = int(sys.argv[2])
filename = '3D_PDF.N'+str(N)+'.c'+str(components)+'.png'
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
pi = np.random.rand(components)
pi = pi/np.sum(pi)
# sequentially build Z up
Z = 0
for n in xrange(components):
    mean = 1 - 2*np.random.rand(2)
    scale = np.random.rand(1)
    Zn = multivariate_normal.pdf(pos, mean, scale*cov)
    if rescale:
        Zn_min = np.min(Zn)
        Zn_range = np.ptp(Zn)
        shift = Zn_min - good_min
        Zn = Zn - shift
        good_scale = good_range/Zn_range
        Zn = good_scale*Zn
    Z = Z + pi[n]*multivariate_normal.pdf(pos, mean, scale*cov)
# normalise
Z = Z/np.sum(Z)

plt.clf()
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='cool', linewidth=0)
plt.savefig(filename)
plt.close()
