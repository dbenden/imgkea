#!/usr/bin/env python

from distutils.core import setup


setup(name='imgkea',
      version='0.1',
      description='Python image processing pipeline',
      author='Daniel Benden',
      author_email='dbenden@danielbenden.nl',
      url='',
      packages=['imgkea', 'imgkea.interfaces'],
      install_requires=['opencv-python', 'picamera2']
     )
