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

import logging
import socketserver
from http import server
from multiprocessing import Process, Queue, get_logger
from queue import Empty

import cv2

from imgkea.interfaces.process import ConsumerProducer, Consumer


logger = get_logger()

class _StreamingHandler(server.BaseHTTPRequestHandler):
    frame = None
    condition = None

    def do_GET(self):
        if self.condition is None:
            raise Exception("No condition set")

        if self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    new_frame = self.frame.get()
                    if new_frame is not None:
                        frame = new_frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()


class _StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


class MJPGStream(ConsumerProducer):
    def __init__(self, port, bufsize=10):
        super().__init__()
        self.handler = _StreamingHandler
        self.condition = Condition()
        self.__frame_queue = Queue()
        self.handler.condition = self.condition
        self.handler.frame = self.__frame_queue
        self.server = _StreamingServer(('', port), self.handler)
        self.__server_process = Process(target=self.server.serve_forever)
        self.__server_process.start()
        self.__buf_size = bufsize

    def clear(self):
        try:
            while self.__frame_queue.qsize() > self.__buf_size:
                self.__frame_queue.get_nowait()
        except Empty:
            pass

    def execute(self, frame):
        res, jpg = cv2.imencode(".jpg", frame.img)
        if res:
            self.clear()
            self.__frame_queue.put(jpg)
        return frame
