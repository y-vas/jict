from jict import jict
import ctypes
from time import sleep
from SharedArray import *

a = attach("shm://test")

while True:
    print(a[0])
    sleep(1)
    
