#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''Flowblade GoPro Proxy Linker 1.0

Author:      Rabit <home@rabits.org>
License:     GPL v3
Description: This script will link your gopro LRV proxies to the flowblade proxy files
Required:    python2.7

Usage:
  1. Run script with path to the proxies
    $ ./flowblade-proxy-gopro.py <LRV_DIR> [ORIG_EXT=.MP4] [PROXY_EXT=.LRV] [PROJECT_RESOLUTION=1920x1080] [PROXY_DIR=$HOME/.flowblade/rendered_clips/proxies]
  2. In the flowblade project mark affected clips & click to render proxies button. In new window select '... & Use existing' and click 'Do render action'
  3. In the Proxy Manager switch project to use proxies
'''

"/home/psa/home/work/video/copter-thirdmk2-flight04/GOPR0222.MP4480264"

import hashlib, os, sys

LRV_DIR = sys.argv[1]

ORIG_EXT = sys.argv[2] if len(sys.argv) > 2 else '.MP4'
PROXY_EXT = sys.argv[3] if len(sys.argv) > 3 else '.LRV'
PROJECT_RESOLUTION = sys.argv[4] if len(sys.argv) > 4 else '1920x1080'
PROXY_DIR = sys.argv[5] if len(sys.argv) > 5 else os.path.join(os.path.expanduser('~'), '.flowblade', 'rendered_clips', 'proxies')

if not os.path.isdir(PROXY_DIR):
    os.makedirs(PROXY_DIR)

if not os.path.isdir(LRV_DIR):
    print 'Error: wrong arguments'
    exit(1)

(proxy_width, proxy_height) = [ int(int(size) * 0.25) for size in PROJECT_RESOLUTION.split('x') ]
proxy_width -= proxy_width % 8
proxy_height -= proxy_height % 8

files = os.listdir(LRV_DIR)

for f in files:
    if f.lower().endswith(PROXY_EXT.lower()):
        print 'Processing %s' % f
        forig = f[:-len(PROXY_EXT)] + ORIG_EXT
        if not forig in files:
            print '  unable to find original file %s' % os.path.join(LRV_DIR, fname + ORIG_EXT)
            exit(1)
        m = hashlib.md5()
        m.update(os.path.join(os.path.abspath(LRV_DIR), forig) + str(proxy_width) + str(proxy_height))
        print os.path.join(os.path.abspath(LRV_DIR), forig) + str(proxy_width) + str(proxy_height)
        link = os.path.join(PROXY_DIR, m.hexdigest()) + ORIG_EXT.lower()
        target = os.path.relpath(os.path.join(LRV_DIR, f), PROXY_DIR)
        print '  create link %s target: %s' % (link, target)
        if os.path.lexists(link):
            os.remove(link)
        os.symlink(target, link)
