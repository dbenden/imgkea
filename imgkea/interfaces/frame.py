from dataclasses import dataclass
import numpy as np

@dataclass
class BoundingBox:
    x: int
    y: int
    w: int
    h: int

    def to_xywh(self):
        return [self.x, self. y, self.w, self.h]

    def to_xyXY(self):
        xX = [self.x, self.x + self.w]
        yY = [self.y, self.y + self.h]
        return  [min(xX), min(yY), max(xX), max(yY)] 

    
@dataclass
class Keypoint:
    x: int
    y: int

    def to_tuple(self):
        return tuple(self.x, self.y)
    
    def to_list(self):
        return [self.x, self.y]

@dataclass
class Frame:
    img: np.ndarray
    frame_nb: int
    width: int
    height: int
    timestamp: float
    boundingbox: list[BoundingBox] = None
    keypoints: list[Keypoint] = None
