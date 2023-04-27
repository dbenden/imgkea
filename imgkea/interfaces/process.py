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

from abc import ABC, abstractmethod
from multiprocessing import Queue, Process



class Consumer(ABC):
    def __init__(self):
        self._queue = Queue()
        self._consumer_process = Process(target=self._run, )
        self._stop = False
   
    def start(self):
        self._consumer_process.start()

    @abstractmethod
    def execute(self, frame):
        return frame

    def _run(self):
        while True:
            item = self._queue.get()
            if item == None:
                break
            f = self.execute(item)

    def consume(self, frame):
        self._queue.put(frame)

    def queue_size(self):
        return self._queue.qsize()

class ConsumerProducer(Consumer):
    def __init__(self):
        super().__init__()
        self._consumers = []

    def register(self, consumer):
        self._consumers.append(consumer)

    @abstractmethod
    def execute(self, frame):
        return frame

    def start(self):
        for consumer in self._consumers:
            consumer.start()
        super().start()

    def _run(self):
        while True:
            item = self._queue.get()
            if item == None:
                break;
            i = self.execute(item)
            for consumer in self._consumers:
                consumer.consume(i)

