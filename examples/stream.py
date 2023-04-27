import sys
sys.path.append('..')

from imgkea.camera import OpenCVCamera
from imgkea.info import FrameInfo
from imgkea.stream import MJPGStream

camera = OpenCVCamera(size=(1024,768), fps=10)
stream = MJPGStream(8000)
#info = FrameInfo()
#info.register(stream)

#camera.register(info)
camera.register(stream)
camera.start()
camera.run()
