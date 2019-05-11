#!/usr/bin/python3

import sys
import os

owndir = os.path.dirname(os.path.realpath(__file__))

# generate concat file for ffmpeg
try:
    with open(os.path.join(owndir, 'data', 'lastid'), 'r') as fh:
        lastid = int(fh.read().strip())

    with open(os.path.join(owndir, 'export', 'netzauktion.ffconcat'), 'w') as fh:
        fh.write('ffconcat version 1.0\n')
        fh.write('file 001.png\n')
        fh.write('duration 2\n')
        for i in range(2, lastid-2):
            fh.write('file {0:03d}.png\n'.format(i))
            fh.write('duration 0.2\n')
        fh.write('file {0:03d}.png\n'.format(lastid-1))
        fh.write('duration 10\n')
        fh.write('file {0:03d}.png\n'.format(lastid-1))
        fh.write('duration 10\n')
except BaseException as e:
    sys.exit(1)
