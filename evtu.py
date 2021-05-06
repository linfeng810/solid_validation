#!/usr/bin/env python3

from vtktools import *
from inTet import pointInside
import numpy as np

# retrieve data
# pressure = self.GetScalarField('Pressure')   # pressure
class evtu(vtu):
    """ 
    enhanced vtu class based on vtktools.py -> vtu.
    
    added method:
    1. newCoordinateatLine: get new spatial coordinate of points that 
        lie on a material line 
    2. getStress: get solid stress @ point p
    """

    def __init__(self, filename = None):
        super(evtu, self).__init__(filename)
        self.nnod = self.ugrid.GetNumberOfPoints()
        self.ncv = self.ugrid.GetNumberOfCells()
        
        """ 
        change coordinate to original coordinate (material coordinate)
        as saved in SolidOriginalCoordinateX/Y/Z
        """
        # material coordinate
        x_orig = np.zeros([self.nnod,3])
        x_orig[:,0] = self.GetScalarField('SolidOriginalCoordinateX')
        x_orig[:,1] = self.GetScalarField('SolidOriginalCoordinateY')
        x_orig[:,2] = self.GetScalarField('SolidOriginalCoordinateZ')


        for i in range (self.nnod):
            newx = x_orig[i, 0]
            newy = x_orig[i, 1]
            newz = x_orig[i, 2]
            self.ugrid.GetPoints().SetPoint(i, newx, newy, newz)


    """    testing if we the change is right  """
    """
    x=self.GetLocations()    # spatial coordinate

    # print difference between material coordinate and spatial coordinate
    err0 = np.linalg.norm(x_orig[:,0]-x[:,0])
    err1 = np.linalg.norm(x_orig[:,1]-x[:,1])
    err2 = np.linalg.norm(x_orig[:,2]-x[:,2])
    print(err0,err1,err2)

    # print difference between new spatial coordinate and spatial coordinate
    x_new=self.GetLocations()
    err0 = np.linalg.norm(x_new[:,0]-x[:,0])
    err1 = np.linalg.norm(x_new[:,1]-x[:,1])
    err2 = np.linalg.norm(x_new[:,2]-x[:,2])
    print(err0,err1,err2)


    # print difference between new spatial coordinate and material coordinate
    err0 = np.linalg.norm(x_new[:,0]-x_orig[:,0])
    err1 = np.linalg.norm(x_new[:,1]-x_orig[:,1])
    err2 = np.linalg.norm(x_new[:,2]-x_orig[:,2])
    print(err0,err1,err2)
    """



    def newCoordinateatLine(self, coordinates):
        """ 
        get spatial coordinate of material points that lie on cylinder axis
        before any deformation
        input:  coordinates [nx3] nparray of point coordinates
        output: probe_origx - material coordinate of points
                probe_diagx - spatial coordinate of points
        output is a tuple of two nparrays
        """
        # parameters to define axia line
        # p1 = (0,0,0)        # start point
        # p2 = (0,0,0.628)    # end point
        # resolution = 50         # 50 sample points

        probe_origx = np.zeros([coordinates.shape[0], 3])
        probe_diagx = np.zeros([coordinates.shape[0], 3])

        probe_origx[:,0] = [self.ProbeData(coordinates, 'SolidOriginalCoordinateX')[i,0] \
                            for i in range(coordinates.shape[0])]
        probe_origx[:,1] = [self.ProbeData(coordinates, 'SolidOriginalCoordinateY')[i,0] \
                            for i in range(coordinates.shape[0])]
        probe_origx[:,2] = [self.ProbeData(coordinates, 'SolidOriginalCoordinateZ')[i,0] \
                            for i in range(coordinates.shape[0])]

        probe_diagx = self.ProbeData(coordinates,'DiagnosticCoordinate')

        return (probe_origx, probe_diagx)

    def getStress(self, p):
        """ 
        get solid stress at given point p (either tuple/list/numpylist is ok.)
        intepolation method: if p is in cell i, return stress in i
        return: stress [3x3] np array
        """

        x=self.GetLocations()    # spatial coordinate
        vtkGhostLevels = self.ugrid.GetCellData().GetArray('vtkGhostLevels')

        # print(self.GetField('StressTenSolid').shape) # -> (200741, 3, 3)

        for i in range(self.ncv):
            v_idx = self.GetCellPoints(i)
            inCell = pointInside(x[v_idx[0],:],x[v_idx[1],:],x[v_idx[2],:],x[v_idx[3],:],p)
            if (inCell and vtkGhostLevels.GetTuple1(i) == 0 ):
                ### if want debug, use these print out lines.
                # print('cell no.\n', i)
                # print('nodes of cell and probing point\n', x[v_idx[:],:], p)
                # print('solid stress tensor inside cell\n', self.GetField('StressTenSolid')[i])
                # print('ghost?', vtkGhostLevels.GetTuple1(i))
                stress = self.GetField('StressTenSolid')[i]
                break
        
        return stress

def lineCoor(p1,p2,resolution):
    """
    Given a line's starting and ending points, and resolution,
    return points coordinates at the line.
    return type: nparray[resolution+1, 3]
    """
    line = np.zeros([resolution+1, 3])
    line[:,0] = [p1[0] + (p2[0] - p1[0])/resolution * i \
                for i in range(resolution+1)]
    line[:,1] = [p1[1] + (p2[1] - p1[1])/resolution * i \
                for i in range(resolution+1)]
    line[:,2] = [p1[2] + (p2[2] - p1[2])/resolution * i \
                for i in range(resolution+1)]
    return line



# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    Taken from: https://stackoverflow.com/a/34325723 by Greenstick
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()