#!/usr/bin/env python

from setuptools import setup, find_packages
from spice2wav import __version__ as spice_ver

setup(
    name='spice-audio-tools',
    version=spice_ver,
    description='Tools to convert from spice to wav and back.',
    author='Marko Vejnovic',
    author_email='contact@markovejnovic.com',
    url='https://github.com/markovejnovic/spice-audio-tools',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'spice2wav=spice2wav.spice2wav:main',
            'wav2spice=spice2wav.wav2spice:main'
        ]
    }
)
