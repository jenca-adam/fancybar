import fancybar,colored
import os,sys
COLOR_TABLE_WIDTH=5
_counter=0
if sys.platform=="win32":
    os.system("cls")
else:
    os.system("clear")

for color in fancybar.COLORS:
    if _counter and _counter%COLOR_TABLE_WIDTH==0:
        print("\n",flush=True)
    hxx=fancybar.COLORS[color]
    rgb=fancybar.parse_hex(hxx)
    if sum(255-i for i in rgb)>sum(rgb) and color!="yellow":
        print(colored.attr("underlined")+colored.bg(color)+colored.fg("white")+color+fancybar.END+colored.attr("res_underlined"),end=" ",flush=True)
    else:
        print(colored.attr("underlined")+colored.bg(color)+colored.fg("black")+color+fancybar.END+colored.attr("res_underlined"),end=" ",flush=True)
    _counter+=1
print()
