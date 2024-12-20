import numpy as np
import math

class SplineSideDetector:

    def __init__(self):
        self.markers = {8:"ears", 26:"neck", 43:"shoulder"}

    def get_ids(self):
        return list(self.markers.keys())
    
    def get_names(self):
        return self.markers.values()
    
    def get_count(self):
        return len(self.markers)
    
    def measure_angle(self,a,b,c):
        v1 = np.array( [a[0]-b[0], a[1]-b[1]] )
        v2 = np.array( [c[0]-b[0], c[1]-b[1]] )

        v1mag = np.sqrt([ v1[0] * v1[0] + v1[1] * v1[1] ])
        v1norm = np.array( [ v1[0] / v1mag, v1[1] / v1mag ] )

        v2mag = np.sqrt([ v2[0] * v2[0] + v2[1] * v2[1] ])
        v2norm = np.array( [ v2[0] / v2mag, v2[1] / v2mag ] )

        dotprod = v1norm[0] * v2norm[0] + v1norm[1] * v2norm[1]
        angle = np.arccos(dotprod)
        return math.degrees(angle)

    def find_angle(self,b,c,angle):
        point_y = np.array([c[1] - b[1]])
        point_x = np.array([c[0] - b[0]])

        shoulder_angle = np.arctan(point_y/point_x)
        shoulder_angle = math.degrees(shoulder_angle)
        neck_angle = angle - shoulder_angle

        return (shoulder_angle,neck_angle)





