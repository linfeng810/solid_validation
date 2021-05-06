#!/usr/bin/env python3

from evtu import *

tmax = 193
# axis
p1 = (0, 0, 0)
p2 = (0, 0, 0.628)
resol = 50

# points
p3 = (0, 0.05, 0.314)
p4 = (0, -0.05, 0.314)

# generate points on line. store their coordinate to nparray "line"
line = lineCoor(p1,p2,resol)

# define objects to store results
f1.open('out1.txt', 'w') # to store material points on 'line' and their spatial coordinates
f2.open('out2.txt', 'w') # to store stress of points p3, p4 and their 

# loop over time steps
for ts in range(tmax+1):
    # The data file
    file_name = "solid_vldt_set6xVelAdapt_"+str(ts)+".pvtu"
    
    t88 = evtu(file_name)

