import mmap
from datetime import datetime as dt

with open("config.json", "r+b") as f:
    mm = mmap.mmap(f.fileno(), 0)

    mm.seek(0)
    print(dt.now())
    print(mm.readline())  # prints b"Hello Python!\n"

    mm.flush()
    mm.close()
