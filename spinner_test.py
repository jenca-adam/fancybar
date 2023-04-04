import fancybar
import cursor
import time
import os
cursor.hide()
for x in range(256):
    for i in fancybar.SPINNERS:
        print(i,fancybar.Spinner(i,1).frames[x%len(fancybar.Spinner(i,1).frames)])
    time.sleep(0.1)
    os.system("clear")
cursor.show()
