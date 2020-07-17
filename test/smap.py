import mmap
from time import time,sleep
from datetime import datetime as dt
from threading import Thread

f = open("config.json", "r+b")
mm = mmap.mmap( f.fileno() , 0 )

while True:
    ns = bytes(str( dt.now() ), 'utf-8')
    nsl = len( ns )

    mm.seek(0)
    mm.resize( nsl )

    mm.write(ns)

    mm.seek(0)

mm.flush()
mm.close()
