import logging
import cv2
from multiprocessing import Process, Condition, Queue, get_logger
from queue import Empty
from http import server
import socketserver

from imgkea.interfaces.process import ConsumerProducer, Consumer


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
                    with self.condition:
                        self.condition.wait()
                        new_frame = self.frame.get_nowait()

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
    def __init__(self, port, bufsize=2):
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
            with self.condition:
                self.clear()
                self.__frame_queue.put(jpg)
                self.condition.notify_all()
        return frame
