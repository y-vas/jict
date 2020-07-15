import mmap

# write a simple example file
with open('config.json', "wb") as f:
    f.write(b"Hello Python!\n")

def read():
    with open("config.json", "r+b") as f:
        mm = mmap.mmap(f.fileno(), 0)

        mm.write(b"Hello vas!\n")
        mm.seek(0)

        print(mm.readline())  # prints b"Hello Python!\n"
        # read content via slice notation
        print(mm[:5])  # prints b"Hello"
        mm[6:] = b" world!\n"
        mm.seek(0)
        print(mm.readline())  # prints b"Hello  world!\n"
        # close the map
        mm.flush()
        mm.close()
