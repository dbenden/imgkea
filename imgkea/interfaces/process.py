from abc import ABC, abstractmethod
from multiprocessing import Queue, Process



class Consumer(ABC):
    def __init__(self):
        self.__queue = Queue()
        self._consumer_process = Process(target=self.__run)
        self.__stop = False
    
    def start(self):
        self._consumer_process.start()

    @abstractmethod
    def execute(self, frame):
        return frame

    def __run(self):
        while True:
            item = self.__queue.get()
            if item == None:
                break;
            f = self.execute(item)

    def consume(self, frame):
        self.__queue.put(frame)

    def queue_size(self):
        return self.__queue.qsize()

class ConsumerProducer(Consumer):
    def __init__(self):
        super().__init__()
        self.__consumers = []

    def register(self, consumer):
        self.__consumers.append(consumer)

    @abstractmethod
    def execute(self, frame):
        return frame

    def start(self):
        for consumer in self.__consumers:
            consumer.start()
        super().start()

    def __run(self):
        while True:
            item = self.__queue.get()
            if item == None:
                break;
            i = self.execute(item)
            for consumer in self.__consumers:
                consumer.consume(i)

