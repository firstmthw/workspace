import cv2
import numpy as np
from cv2 import aruco
import matplotlib.pyplot as plt
from CaptureDevice import *

class CharucoCalibrator:
    
    def __init__(self, perimeter_rate):
        self._marker_list = []   
        self.aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
        self.squareX = 10               # Number of markers in X direction
        self.squareY = 10               # Number of markers in Y direction
        self.squareLength = 0.015       # Squre length (in meter)
        self.markerLength = 0.01       # Marker length (in meter)
        self.charuco_board = aruco.CharucoBoard_create(self.squareX, self.squareY, self.squareLength, self.markerLength, self.aruco_dict)
        self.parameters =  aruco.DetectorParameters_create()
        self.parameters.cornerRefinementMethod = aruco.CORNER_REFINE_SUBPIX
        self.parameters.cornerRefinementMinAccuracy = 0.05
        self.parameters.minMarkerPerimeterRate = perimeter_rate #ใส่เป็นค่าคงที่ไม่ได้ต้องใส่เป็นตัวแปร
        self.cameraMatrix = None
        self.distCoeffs = None


    def append(self,img):
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
        corners, ids, _ = aruco.detectMarkers(gray_img, self.aruco_dict, parameters=self.parameters)
        if ids is None:
            return len(self._marker_list)
        if len(ids) >= 45:
            marker = {"img":gray_img,"corners":corners,"ids":ids}
            self._marker_list.append(marker) #มีรูปใหม่เพิ่มเข้ามาเรื่อยๆ
            
            print(len(self._marker_list))
        return len(self._marker_list)

    def clear(self): 
        self._marker_list = [] #พอไม่ใช้แล้วต้องล้างข้อมูลทิ้ง

    def length(self): #ดูว่ามีข้อมูลเท่าไหร่ถ้ารูปไม่พอก็จะได้appendต่อ
        return len(self._marker_list)
    
    def calibrate(self):
        corners_all = []
        ids_all = []
        print (self._marker_list[0]['corners'])

        for i in range(len(self._marker_list)):
            ret, charuco_corners, charuco_ids = aruco.interpolateCornersCharuco(
                markerCorners=self._marker_list[i]['corners'],
                markerIds=self._marker_list[i]['ids'],
                image=self._marker_list[i]['img'],
                board=self.charuco_board)
            corners_all.append(charuco_corners)
            ids_all.append(charuco_ids)
       
        print("corners_all", corners_all[0]) 
        print("ids_all", ids_all[0])

        flags = cv2.CALIB_RATIONAL_MODEL
        image_size = (self._marker_list[0]['img'].shape[0], self._marker_list[0]['img'].shape[1])
        calibration, cameraMatrix, distCoeffs, rvecs, tvecs = aruco.calibrateCameraCharuco(
            charucoCorners=corners_all,
            charucoIds=ids_all,
            board=self.charuco_board,
            imageSize=image_size,
            cameraMatrix=self.cameraMatrix, 
            distCoeffs=self.distCoeffs,
            flags=flags)
        
        self.cameraMatrix = cameraMatrix
        self.distCoeffs = distCoeffs

        print("calibration", calibration)
        print("cameraMatrix", cameraMatrix)
        return (calibration, cameraMatrix, distCoeffs, rvecs, tvecs, ids_all, corners_all)
    
    def test(self,img):
        test_marker = self._marker_list[-1] #เอารูปที่เก็บไว้มาใช้    
        rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(test_marker["corners"], self.markerLength, self.cameraMatrix, self.distCoeffs)
        estimatePoseSingleMarkers = test_marker["ids"]
        if tvecs is not None:      
            print("tvecs", tvecs)
        pass  

    def measure(self,img,aruco_ids):
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
        corners, ids, _ = aruco.detectMarkers(gray_img, self.aruco_dict, parameters=self.parameters)
        if ids is None:
            return None
        aruco_pose = {"ids":[],"tvecs":[],"corners":[],"rvecs":[]}
        for i in range(len(ids)):
            if ids[i] in aruco_ids:
                aruco_pose["ids"].append(ids[i])
                rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(corners[i], self.markerLength, self.cameraMatrix, self.distCoeffs)
                aruco_pose["corners"].append(corners[i])
                aruco_pose["tvecs"].append(tvecs)
                aruco_pose["rvecs"].append(rvecs)
 
        return aruco_pose
    


