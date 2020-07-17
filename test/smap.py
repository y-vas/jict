import mmap
from time import time,sleep
from datetime import datetime as dt
from threading import Thread

with open("config.json", "r+b") as f:
    mm = mmap.mmap(f.fileno(), 0 )

    while True:
        ns = bytes(str( dt.now() ), 'utf-8')
        nsl = len( ns )

        mm.seek(0)
        mm.resize( nsl )

        mm.write(ns)

        mm.seek(0)
        print(mm.readline())  # prints b"Hello Python!\n"
        # sleep(0.1)

    mm.flush()
    mm.close()
