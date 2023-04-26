from imgkea.interfaces.process import ConsumerProducer, Consumer


class FrameInfo(ConsumerProducer):
    def __init__(self):
        super().__init__()

    def execute(self, frame):
        print(f"Frame [{frame.frame_nb}] ts = {frame.timestamp} : width = {frame.width} height = {frame.height} queue length {self.queue_size()}") 
        return frame
