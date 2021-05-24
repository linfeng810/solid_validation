#!/usr/bin/env python3

from evtu import *

ss = 1e-5

tmax = 10
# axis
p1 = (0, 0, 0)
p2 = (0, 0, 0.628)
resol = 50

# points to retrieve stress state.
p3 = (0, 0.05-ss, 0.314)
p4 = (0, -0.05+ss, 0.314)

# generate points on line. store their coordinate to nparray "line"
line = lineCoor(p1,p2,resol)

# define objects to store results
f1 = open('out1.txt', 'w') # to store material points on 'line' and their spatial coordinates
# f2 = open('out2.txt', 'w') # to store stress of points p3, p4 and their 
x_mat = np.zeros([line.shape[0], 3])    # to store material coordinate
x_spatial = np.zeros([line.shape[0], 3])    # to store spatial coordinate

# loop over time steps

# a prograss indication bar
printProgressBar(0, tmax+1, prefix = 'Progress', suffix = 'Complete', length = 50)

for ts in range(tmax+1):
    # The data file
    file_name = "/mnt/c/Users/jztc0/Desktop/test/stress_veri/fix-two-end+gravity/solidity_results_for_postprocessing_script/LL"\
	+str(ts)+".vtu"
    #"solid_vldt_set6xVelAdapt_"+str(ts)+".pvtu"
    if (ts==0):
        t88 = evtu(file_name)
        state = t88.getMaterialCoordinate()
        for i in range(line.shape[0]):
            # write material coordinate
            f1.write('%16.10e\t%16.10e\t%16.10e\t'%(line[i,0],line[i,1],line[i,2]))
        f1.write('\n')
        continue
    else:
        t88 = evtu(file_name, state)

    # new coordinate
    x_spatial=t88.newCoordinateatLine(line)
    
    for i in range(x_mat.shape[0]):
        f1.write('%16.10e\t%16.10e\t%16.10e\t'%(x_spatial[i,0], x_spatial[i,1], x_spatial[i,2]))
    f1.write('\n')

    # # stress at points
    # for p in (p3,p4):
    #     stress = t88.getStress(p)
    #     [f2.write('%16.10e\t'%stress[i,j]) for i in range(3) for j in range(3)]
    # f2.write('\n')

    # update progress bar
    printProgressBar(ts, tmax+1, prefix = 'Progress', suffix = 'Complete', length = 50)

f1.close()
# f2.close()
