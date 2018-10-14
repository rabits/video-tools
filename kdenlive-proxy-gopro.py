#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''Kdenlive GoPro Proxy Linker 1.0

Author:      Rabit <home@rabits.org>
License:     GPL v3
Description: This script will link your gopro LRV proxies to the kdenlive proxy files
Required:    python2.7 / python 3

Usage:
  1. Execute script in your project folder:
    $ ./kdenlive-proxy-gopro.py <LRV_DIR> [ORIG_EXT=.MP4] [PROXY_EXT=.LRV] [PROXY_DIR=LRV_DIR/proxy]
  2. Create new or use existing kdenlive project
  3. Disable autocreation of proxies and change proxy ext to 'mp4' in your project settings
  4. Select all gopro files and run proxy recreation
'''

import hashlib, os, sys

LRV_DIR = sys.argv[1]

ORIG_EXT = sys.argv[2] if len(sys.argv) > 2 else '.MP4'
PROXY_EXT = sys.argv[3] if len(sys.argv) > 3 else '.LRV'
PROXY_DIR = sys.argv[4] if len(sys.argv) > 4 else os.path.join(LRV_DIR, 'proxy')

if not os.path.isdir(PROXY_DIR):
    os.makedirs(PROXY_DIR)

if not os.path.isdir(LRV_DIR):
    print('Error: wrong arguments')
    exit(1)

files = os.listdir(LRV_DIR)

for f in files:
    if f.lower().endswith(PROXY_EXT.lower()):
        print('Processing %s' % f)
        forig = f[:-len(PROXY_EXT)] + ORIG_EXT
        if not forig in files:
            print('  unable to find original file %s' % os.path.join(LRV_DIR, forig))
            exit(1)
        m = hashlib.md5()
        forig = os.path.join(LRV_DIR, forig)
        fsize = os.path.getsize(forig)
        with open(forig, "rb") as fd:
            if fsize > 1000000*2:
                m.update(fd.read(1000000))
                fd.seek(fsize - 1000000)
            m.update(fd.read())
        link = os.path.join(PROXY_DIR, m.hexdigest()) + ORIG_EXT.lower()
        target = os.path.relpath(os.path.join(LRV_DIR, f), PROXY_DIR)
        print('  create link %s target: %s' % (link, target))
        if os.path.lexists(link):
            os.remove(link)
        os.symlink(target, link)
