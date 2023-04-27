#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                    Version 2, December 2004
#
# Copyright (C) 2023 Benden, Daniel <dbenden@danielbenden.nl>
#
# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
#  0. You just DO WHAT THE FUCK YOU WANT TO.

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

from typing import Any
from dataclasses import dataclass

import numpy as np


@dataclass
class BoundingBox:
    x: int  # pylint: disable=invalid-name
    y: int  # pylint: disable=invalid-name
    w: int  # pylint: disable=invalid-name
    h: int  # pylint: disable=invalid-name
    label: str

    def to_xywh(self):
        return [self.x, self. y, self.w, self.h]

    def to_xyXY(self):
        xX = [self.x, self.x + self.w]  # pylint: disable=invalid-name
        yY = [self.y, self.y + self.h]  # pylint: disable=invalid-name
        return [min(xX), min(yY), max(xX), max(yY)]


@dataclass
class Keypoint:
    x: int  # pylint: disable=invalid-name
    y: int  # pylint: disable=invalid-name

    label: str

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
    userdata: dict[str, Any]

    def tobytes(self):
        return self.img.tobytes()
