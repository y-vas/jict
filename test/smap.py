import mmap

# write a simple example file
with open('config.json', "wb") as f:
    f.write(b"Hello Python!\n")

with open("config.json", "r+b") as f:
    mm = mmap.mmap(f.fileno(), 0 )

    ns = b"Hello vasafsdfasdfasdfasdfalyyl!\n"
    nsl = len(ns)
    print(nsl)

    mm.seek(0)
    mm.resize( nsl )

    mm.write(ns)

    mm.seek(0)
    print(mm.readline())  # prints b"Hello Python!\n"
    mm.flush()
    mm.close()
