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

from imgkea.interfaces.process import Consumer, ConsumerProducer


class FrameInfo(ConsumerProducer):
    def __init__(self):
        super().__init__()

    def execute(self, frame):
        print(f"Frame [{frame.frame_nb}] ts = {frame.timestamp} : width = {frame.width}"
              f"height = {frame.height} queue length {self.queue_size()}")
        return frame
