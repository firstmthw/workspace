import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from scipy import interpolate

class SplineBackDetector:

    def __init__(self):
        self.markers = {2:"C7", 8:"T3", 12:"T5", 17:"T7", 21:"T9", 27:"T11", 32:"L1", 38:"L3", 43:"L5", 49:"S2"}

    def get_ids(self):
        return list(self.markers.keys())
    
    def get_names(self):
        return self.markers.values()
    
    def get_count(self):
        return len(self.markers)
    
    def spline(self,points):
        #print(points)
        x = []
        y = []
        for i in range(len(points)):
            x.append(points[i][0])
            y.append(points[i][1])
        #print(x,y)
        tck,u = interpolate.splprep([x,y],s=0)
        u_new = np.linspace(u.min(),u.max(),100)
        x_new,y_new = interpolate.splev(u_new,tck,der=0)
        #print(x_new,y_new)
        return x_new,y_new