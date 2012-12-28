#!/bin/bash

gpio -g mode 22 in

if [ $(gpio -g read 22) = 1 ]
then
	sudo python /home/pi/.config/pianobar/scripts/ButtonWatcher.py
fi
