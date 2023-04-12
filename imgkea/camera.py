import cv2
import numpy as np

from camimg.interfaces.source import Camera

class OpenCVCamera(Camera):
    def __init__(self, 
                 camera_id: int = 0, 
                 size: tuple[int, int] = (640,480), 
                 fps: int = 30):

        super().__init__()
        self.__camera_id = camera_id
        self.__src = cv2.VideoCapture(self.__camera_id)
        self.__src.set(cv2.CAP_PROP_FRAME_WIDTH, size[0])
        self.__src.set(cv2.CAP_PROP_FRAME_HEIGHT, size[1])
        self.__src.set(cv2.CAP_PROP_FPS, fps)
    def get_image(self):
            ret, frame = self.__src.read()
            if ret:
                return frame
            return None
