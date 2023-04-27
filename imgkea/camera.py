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

import cv2

from imgkea.interfaces.source import Camera

class OpenCVCamera(Camera):
    def __init__(self,
                 camera_id: int = 0,
                 size: tuple[int, int] = (640, 480),
                 fps: int = 30):

        super().__init__()
        self.__camera_id = camera_id
        self.__src = cv2.VideoCapture(self.__camera_id)
        self.__src.open(self.__camera_id, cv2.CAP_ANY)
        self.__src.set(cv2.CAP_PROP_FRAME_WIDTH, size[0])
        self.__src.set(cv2.CAP_PROP_FRAME_HEIGHT, size[1])
        self.__src.set(cv2.CAP_PROP_FPS, fps)

    def get_image(self):
        ret, frame = self.__src.read()
        if ret:
            return frame
        return None
