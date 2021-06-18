#!/usr/bin/env python3

from evtu import *

ss = 1e-5

tstart = 00
tmax = 190
tstep = 10
# axis
p1 = (0, 0, 0)
p2 = (0, 0, 0.628)
resol = 50

# points
p3 = (0, 0.05-ss, 0.314)
p4 = (0, -0.05+ss, 0.314)

# generate points on line. store their coordinate to nparray "line"
line = lineCoor(p1,p2,resol)
print(line)

# define objects to store results
f1 = open('out1.txt', 'w') # to store material points on 'line' and their spatial coordinates
# f2 = open('out2.txt', 'w') # to store stress of points p3, p4 and their 
# x_mat = np.zeros([line.shape[0], 3])
x_spatial = np.zeros([line.shape[0], 3])

# loop over time steps

# a prograss indication bar
printProgressBar(tstart, tmax+1, prefix = 'Progress', suffix = 'Complete', length = 50)

file_directory = '/data/linfeng/data2/module_vldt/z18_gravity/liang/z02-nonlinear5/restart2/'
# '/data/linfeng/data2/module_vldt/z18_gravity/fix-two-ends/finer-uniform-adapt/restart-from-500/'

for ts in range(tstart,tmax+tstep, tstep):
    # The data file
    file_name = file_directory + "solid_vldt_set6+6100_"+str(ts)+".pvtu"
    #"solid_vldt_set6xVelAdapt_"+str(ts)+".pvtu"
    t88 = evtu(file_name)
    # new coordinate
    x_spatial=t88.newCoordinateatLine(line)
    if (ts==0):
        for i in range(line.shape[0]):
            f1.write('%16.10e\t%16.10e\t%16.10e\t'%(line[i,0], line[i,1], line[i,2]))
        f1.write('\n')
        continue
    else:
        for i in range(x_spatial.shape[0]):
            f1.write('%16.10e\t%16.10e\t%16.10e\t'%(x_spatial[i,0], x_spatial[i,1], x_spatial[i,2]))
        f1.write('\n')

    # # stress at points
    # for p in (p3,p4):
    #     stress = t88.getStress(p)
    #     [f2.write('%16.10e\t'%stress[i,j]) for i in range(3) for j in range(3)]
    # f2.write('\n')

    # update progress bar
    printProgressBar(ts, tmax+1, prefix = 'Progress', suffix = 'Complete', length = 50)

f1.write(file_directory)
f1.write('\ntmax = %d\n'%tmax)
f1.write('tstep = %d'%tstep)
f1.close()
# f2.close()
