#!/usr/bin/python3
# unzip and zero out zip as it uncompresses to save diskspace
# mobman
# int fallocate(int fd, int mode, off_t offset, off_t len)
import ctypes
libc = ctypes.cdll.LoadLibrary("libc.so.6")
fallocate = libc.fallocate
fallocate.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.c_longlong, ctypes.c_longlong)
FALLOC_FL_PUNCH_HOLE = 2
FALLOC_FL_KEEP_SIZE = 1

import sys, subprocess, zipfile  # will need zlib for compression
myzip = sys.argv[1]
fd = open(myzip,"r+")
fno = fd.fileno()
zf = zipfile.ZipFile(myzip, 'r')
for info in zf.infolist():
   zf.extract(info)
   # print(info.header_offset,info.compress_size)
   rc = fallocate(fno, FALLOC_FL_PUNCH_HOLE|FALLOC_FL_KEEP_SIZE,
                  info.header_offset, info.compress_size)
   if rc!=0: print("fallocate failed\n")
   subprocess.call("ls -ls "+myzip,shell=True)
