#!/bin/sh
# asciinema go brrrrr

asciinema rec spin --rows 86 -c "python spinner_test.py;exit"
agg spin spinners.gif

