for i in *.gif;do echo $i;convert -loop 0 $i $i;done
