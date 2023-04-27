# Copyright (C) 2023  Benden, Daniel <dbenden@danielbenden.nl>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
