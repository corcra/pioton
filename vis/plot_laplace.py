#!/usr/bin/python
# Plot a laplace distribution with specified parameters.

import numpy as np
import matplotlib.pyplot as plt
import sys

t_green = '#009933'

# params
mu = int(sys.argv[1])
b = int(sys.argv[2])

# generate samples
# lots of samples are a lazy-man's smoothing
lap_X = np.random.laplace(loc=mu, scale=b, size=1000000)

# plotting!
fig = plt.figure()
h = plt.hist(lap_X, bins=500, alpha=1.0, color=t_green, normed=True, histtype='stepfilled', antialiased=True, linewidth=0)
# to make the plot symmetric, find maximum distance to centre
lower_dx = mu - h[1][0]
upper_dx= h[1][-1] - mu
max_dx = np.max([abs(lower_dx), abs(upper_dx)])
plt.xlim(-max_dx + mu, max_dx +mu)
# labels etc.
plt.title('Laplace distribution with mu = '+str(mu)+' and b = '+str(b), family='monospace', size=16)
plt.xlabel('x', family='monospace', size=16)
plt.ylabel('p(x)', family='monospace', size=16)
plt.tight_layout()      # requires Agg
plt.savefig('laplace_mu'+str(mu)+'_b'+str(b)+'.png', dpi=200)
