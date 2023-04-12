import cv2
import numpy as np
import logging
from camimg.interfaces.process import ConsumerProducer, Consumer


class FrameInfo(Consumer):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger("Info")

    def execute(self, frame):
        print(f"Frame [{frame.frame_nb}] ts = {frame.timestamp} : width = {frame.width} height = {frame.height} queue length {self.queue_size()}") 




