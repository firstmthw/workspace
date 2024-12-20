import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import cv2
import sys

class CaptureDevice():

    def __init__(self, cam_ID):
        self.video_size = (1920, 1080)
        self.preview_size = (640, 360)
        self.capture = cv2.VideoCapture(cam_ID)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.video_size[0])
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.video_size[1])
        self._frame = None
        self._preview = None

    def read(self):
        _, self._frame = self.capture.read()

    def preview(self):
        
        if self._frame is not None:
            self._preview = cv2.resize(self._frame, self.preview_size)
            self._preview = cv2.flip(self._preview, 1)
            self._preview = cv2.cvtColor(self._preview, cv2.COLOR_BGR2RGB)
            
        else:
            self._preview = None

        return self._preview

    def raw_image(self):
        return self._frame
    
    
        
        
