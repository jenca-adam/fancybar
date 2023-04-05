import fancybar
import cursor
import time
import os
import sys:
cursor.hide()
def cl():
    if sys.platform=="win32":
        os.system("cls")
    else:
        os.system("clear")
for x in range(256):
    for i in fancybar.SPINNERS:
        print(i,fancybar.Spinner(i,1).frames[x%len(fancybar.Spinner(i,1).frames)])
    time.sleep(0.1)
    cl()
cursor.show()
