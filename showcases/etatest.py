import fancybar,time

a=fancybar.ProgressBar(100)

with a:
    for i in range(100):
        time.sleep(0.1)
        a.update()
        print(a.eta)
        
