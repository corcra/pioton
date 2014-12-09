#!/usr/bin/python
# Plot a laplace distribution with specified parameters.

import numpy as np
from scipy.stats import laplace
import matplotlib.pyplot as plt
import sys

t_green = '#009933'

# params
mu = int(sys.argv[1])
b = int(sys.argv[2])

# generate samples
# lots of samples are a lazy-man's smoothing
lap_X = laplace.rvs(loc=mu, scale=b, size=1000000)
x = np.linspace(start=-8*b,stop=8*b,num=1000000)
lap_Q = laplace.cdf(x=x, loc=mu, scale=b)

# plotting pdf!
fig = plt.figure()
h = plt.hist(lap_X, bins=500, alpha=1.0, color=t_green, normed=True, histtype='stepfilled', antialiased=True, linewidth=0)
# to make the plot symmetric, find maximum distance to centre
lower_dx = mu - h[1][0]
upper_dx= h[1][-1] - mu
max_dx = np.max([abs(lower_dx), abs(upper_dx)])
plt.xlim(-max_dx + mu, max_dx +mu)
# labels etc.
plt.title('Laplace PDF with mu = '+str(mu)+' and b = '+str(b), family='monospace', size=16)
plt.xlabel('x', family='monospace', size=16)
plt.ylabel('p(x)', family='monospace', size=16)
plt.tight_layout()      # requires Agg
plt.savefig('laplacePDF_mu'+str(mu)+'_b'+str(b)+'.png', dpi=200)
plt.clf()

# plotting cdf!
fig = plt.figure()
#h = plt.plot(x, lap_Q, color=t_green, linestyle='solid')
h = plt.fill_between(x, 1-lap_Q, 0, color=t_green, linestyle='solid')
plt.title('Laplace CDF with mu = '+str(mu)+' and b = '+str(b), family='monospace', size=16)
plt.xlabel('C', family='monospace', size=16)
plt.ylabel('p(x > C)', family='monospace', size=16)
plt.ylim(0,1.1)
plt.xlim(-8*b,8*b)
plt.savefig('laplaceCDF_mu'+str(mu)+'_b'+str(b)+'.png', dpi=200)
plt.clf()
