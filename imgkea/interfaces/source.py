import time
from abc import ABC, abstractmethod
import numpy as np
from .frame import Frame


class Camera(ABC):
    def __init__(self):
        self.__consumers = []
    
    def register(self, consumer):
        self.__consumers.append(consumer)
    
    @abstractmethod
    def get_image(self):
        return np.ndarray((10,10))

    def start(self):
        for consumer in self.__consumers:
            consumer.start()

    def run(self):
        c = 0
        t0 = time.time()
        while True:
            image = self.get_image()
            h,w  = image.shape[:2]
            
            frame = Frame(img=image,
                          width = w,
                          height = h,
                          frame_nb = c,
                          timestamp = time.time() - t0)
            c += 1

            for consumer in self.__consumers:
                consumer.consume(frame)
