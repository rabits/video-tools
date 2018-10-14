#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''Kdenlive GoPro Proxy Linker 1.0

Author:      Rabit <home@rabits.org>, Andrii Danyleiko <andrii.danyleiko@gmail.com>
License:     GPL v3
Description: This script will link your gopro LRV proxies to the kdenlive proxy files
Required:    python2.7 / python 3

Usage:
  1. Execute script in your project folder:
    $ ./kdenlive-proxy-gopro.py <PROJ_DIR> [ORIG_EXT=.MP4] [PROXY_EXT=.LRV] [PROXY_DIR=PROJ_DIR/proxy]
  2. Create new or use existing kdenlive project
  3. Disable autocreation of proxies and change proxy ext to 'mp4' in your project settings
  4. Select all gopro files and run proxy recreation
'''

import os
import hashlib
import argparse

parser = argparse.ArgumentParser(description="Link gopro lrv files as proxies for kdenlive", epilog=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("proj_dir", help="Path to project dir, where oriinal files located", metavar='PROJ_DIR')
parser.add_argument("orig_ext", nargs='?', help="File extension of original gopro files, case sensitive (default: %(default)s)", metavar='ORIG_EXT', default='.MP4')
parser.add_argument("lrv_ext", nargs='?', help="File extension of lrv gopro files, case insensitive (default: %(default)s)", metavar='PROXY_EXT', default='.LRV')
parser.add_argument("proxy_dir", nargs='?', help="File extension of original gopro files (default: <PROJ_DIR>/proxy)", metavar='PROXY_DIR', default=None)
parser.add_argument("-l", "--lrv-dir", help="Path to separate dir with LRV files if they are not placed with original files (default: <PROJ_DIR>)", metavar='LRV_DIR', default=None)

args = parser.parse_args()
args.proxy_dir = args.proxy_dir or os.path.join(args.proj_dir, 'proxy')
args.lrv_dir = args.lrv_dir or args.proj_dir

for dir_path in (args.proj_dir, args.lrv_dir):
    if not os.path.isdir(dir_path):
        print('Dir "%s" does not exist' % dir_path)
        exit(1)

if not os.path.isdir(args.proxy_dir):
    print('Proxy dir "%s" created' % args.proxy_dir)
    os.makedirs(args.proxy_dir)

proj_files = [f for f in os.listdir(args.proj_dir) if f.lower().endswith(args.orig_ext.lower())]
lrv_files = (lrv for lrv in os.listdir(args.lrv_dir) if lrv.lower().endswith(args.lrv_ext.lower()))

for lrv in lrv_files:
    print('Processing %s/%s' % (args.lrv_dir, lrv))
    f_orig = lrv[:-len(args.lrv_ext)] + args.orig_ext
    if not f_orig in proj_files:
        print('  unable to find original file %s' % os.path.join(args.proj_dir, f_orig))
        exit(1)
    m = hashlib.md5()
    f_orig = os.path.join(args.proj_dir, f_orig)
    fsize = os.path.getsize(f_orig)
    with open(f_orig, "rb") as fd:
        if fsize > 1000000*2:
            m.update(fd.read(1000000))
            fd.seek(fsize - 1000000)
        m.update(fd.read())
    link = os.path.join(args.proxy_dir, m.hexdigest()) + args.orig_ext.lower()
    target = os.path.relpath(os.path.join(args.proj_dir, lrv), args.proxy_dir)
    if os.path.lexists(link):
        print('  remove old link %s' % link)
        os.remove(link)
    print('  create link %s target: %s' % (link, target))
    os.symlink(target, link)
