import fancybar,time,random

for bartype in fancybar.BARTYPES:
    if bartype=="nobar":
        continue
    print(bartype)
    if bartype=="gradient":
        length=100
    else:
        length=50
    for i in fancybar.SequentialProgressBar(range(100),bartype=bartype,length=length):
        time.sleep(random.randrange(10)/100)

