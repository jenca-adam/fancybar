import fancybar,time,random
for i in fancybar.bar(range(100),spinner="timeTravel",spinner_speed=0.25,percentage_fg_color="red",percentage_bg_color="white",spinner_fg_color="white",bartype="gradient",start_color=(42,0,69),end_color=(255,255,0)):
    time.sleep(0.01)

