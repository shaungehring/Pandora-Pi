#!/usr/bin/env python
 
import sys, serial, time, os, socket
from time import sleep
from random import randint
from subprocess import Popen
import pandoraUtils
import pickle
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.IN) # Skip Song
GPIO.setup(3, GPIO.IN) # Change Station
GPIO.setup(4, GPIO.IN) # Vol -
GPIO.setup(17, GPIO.IN) # Vol +
GPIO.setup(27, GPIO.IN) # Play/Pause
GPIO.setup(22, GPIO.IN) # Menu

scripts_folder_location = '/home/pi/.config/pianobar/scripts/'
fifo_folder_location = '/home/pi/.config/pianobar/ctl'

LCD = serial.Serial('/dev/ttyAMA0', 9600)

total_stations = 32
current_station = 7

allow_lcd_update = True
forceUpdate = False

playing_stream = "Playing"

current_screen = "default"

def main():

	global playing_stream
	global current_screen

	pandoraUtils.writeToLCD("Pandora Pi", "Starting")
	
	sleep(4)
	
	pandoraUtils.parseAndWrite()

	while True:

		# Default Page

		if ( GPIO.input(2) == False  and current_screen == "default"):
			
			pandoraUtils.log('Button 1 - Skip Song')
			pandoraUtils.writeToLCD("Skipping", "Song")
			os.system('echo "n" >> ' + fifo_folder_location)

		if ( GPIO.input(3) == False  and current_screen == "default"):

			pandoraUtils.log('Button 2 - Skip Station')
			pandoraUtils.writeToLCD("Next", "Station")
			current_station = randint(1,total_stations)
			os.system('echo "s' + str(current_station) + '" >> ' + fifo_folder_location)

			parseAndWrite(8, True)

			parseAndWrite(3)


		if ( GPIO.input(4)== False  and current_screen == "default"):

			pandoraUtils.log('Button 3 - Vol Down')
			pandoraUtils.writeToLCD("Volume", "Down")
			os.system('echo "((((" >> ' + fifo_folder_location)

			sleparseAndWriteep(2)


		if ( GPIO.input(17)== False  and current_screen == "default"):

			pandoraUtils.log('Button 4 - Vol Up')
			pandoraUtils.writeToLCD("Volume", "Up")
			os.system('echo "))))" >> ' + fifo_folder_location)

			parseAndWrite(2)


		if ( GPIO.input(27)== False  and current_screen == "default"):

			pandoraUtils.log('Button 5 - Play/Pause')

			if playing_stream == "Playing":
				pandoraUtils.writeToLCD("Paused", "")
				playing_stream = "Paused"
			else:
				pandoraUtils.writeToLCD("Playing", "")
				playing_stream = "Playing"
				parseAndWrite(2)

			os.system('echo "p" >> ' + fifo_folder_location)

			
		if ( GPIO.input(22)== False  and current_screen == "default"):

			pandoraUtils.log('Button 6 - Menu')
			
			pandoraUtils.writeToLCD("Pandora Pi", "Menu")
			sleep(.75)

			pandoraUtils.writeToLCD("1:Like 2:Dislike", "3:IP 4:Next Pg")
			current_screen = "menupg1"

		# Menu Page 1

		if ( GPIO.input(2) == False  and current_screen == "menupg1"):

			pandoraUtils.log('Button 6 - Menu - Sub 1 - Like')
			pandoraUtils.writeToLCD("Liking", pandoraUtils.getShared("song"))
			os.system('echo "+" >> ' + fifo_folder_location)

			parseAndWrite(2)
			

		if ( GPIO.input(3) == False  and current_screen == "menupg1"):

			pandoraUtils.log('Button 6 - Menu - Sub 2 - DisLike')
			pandoraUtils.writeToLCD("Disliking", pandoraUtils.getShared("song"))
			os.system('echo "-" >> ' + fifo_folder_location)

			parseAndWrite(2)

		if ( GPIO.input(4) == False  and current_screen == "menupg1"):

			pandoraUtils.log('Button 6 - Menu - Sub 3 - IP Address')
			getIPAddress()

			parseAndWrite(5)


		if ( GPIO.input(17) == False  and current_screen == "menupg1"):

			pandoraUtils.writeToLCD("1:Prev Pg 2:Cur St", "3:Off 4:Next Pg")
			current_screen = "menupg2"

		# Menu Page 2

		if ( GPIO.input(2) == False  and current_screen == "menupg2"):

			pandoraUtils.log('Button 6 - Menu - Sub 1 - Menu Pg 1')
			pandoraUtils.writeToLCD("1:Like 2:Dislike", "3:IP 4:Next Pg")
			current_screen = "menupg1"

		if ( GPIO.input(3) == False  and current_screen == "menupg2"):

			pandoraUtils.log('Button 6 - Menu - Sub 2 - Station Name')
			pandoraUtils.writeToLCD(pandoraUtils.getShared("stationName"), "")

			parseAndWrite(2)

		# if ( GPIO.input(4) == False  and current_screen == "menupg2"):

		# 	pandoraUtils.log('Button 6 - Menu - Sub 3 - Shutdown')
		# 	pandoraUtils.writeToLCD("Shutting Down", "Thanks")
		# 	pianobarProcess.terminate()
		# 	# os.system('echo "q" >> ' + fifo_folder_location)

		# 	sleep(2)

		# 	pandoraUtils.writeToLCD("Pandora Pi: OFF", "1: Turn ON")
		# 	current_screen = "off"

		# if ( GPIO.input(2) == False  and current_screen == "off"):

		# 	pianobarProcess = Popen('sudo -u pi pianobar', shell=True)

		# 	PandoraUtils.writeToLCD("Pandora Pi", "Starting")
			
		# 	current_screen = "default"

		# 	sleep(4)
	
		# 	pandoraUtils.parseAndWrite()


		sleep(.25)

def parseAndWrite(secDelay = 0, changedStation = False):

	global current_screen

	current_screen = "default"

	sleep(secDelay)

	pandoraUtils.parseAndWrite(changedStation)

def getIPAddress():

	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(('google.com', 0))
	IPaddr = s.getsockname()[0]

	pandoraUtils.writeToLCD("IP Address:", IPaddr)

main()