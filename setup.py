#!/usr/bin/env python

from distutils.core import setup

setup(name='EPMCLib',
      version='0.1',
      description='Python client for EuropePMC API',
      author='Thomas Arrow',
      author_email='thomasarrow@gmail.com',
      url='https://github.com/tarrow/epmclib',
      packages=['epmclib'],
      install_requires=['requests'],
     )