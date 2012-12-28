#!/usr/bin/env python
 
import sys, serial, time, os, socket
from time import sleep
from random import randint
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.IN) # Skip Song
GPIO.setup(3, GPIO.IN) # Change Station
GPIO.setup(4, GPIO.IN) # Vol -
GPIO.setup(17, GPIO.IN) # Vol +
GPIO.setup(27, GPIO.IN) # Play/Pause
GPIO.setup(22, GPIO.IN) # Menu

LCD = serial.Serial('/dev/ttyAMA0', 9600)

total_stations = 32
current_station = 7

current_song = ""
current_artist = ""
current_station_name = ""

allow_lcd_update = True
forceUpdate = False

playing_stream = "Playing"

def main():

	global playing_stream
	global forceUpdate

	writeToLCD("Pandora Pi", "Starting")
	
	sleep(4)
	
	parseAndWrite()

	while True:

		if ( GPIO.input(2) == False ):
			
			log('Button 1 - Skip Song')
			writeToLCD("Skipping", "Song")
			os.system('echo "n" >> /home/pi/.config/pianobar/ctl')

		if ( GPIO.input(3) == False ):

			log('Button 2 - Skip Station')
			writeToLCD("Next", "Station")
			current_station = randint(1,total_stations)
			os.system('echo "s' + str(current_station) + '" >> /home/pi/.config/pianobar/ctl')

			sleep(8)

			parseAndWrite(True)

			sleep(3)

			parseAndWrite()

		if ( GPIO.input(4)== False ):

			log('Button 3 - Vol Down')
			writeToLCD("Volume", "Down")
			os.system('echo "((((" >> /home/pi/.config/pianobar/ctl')

			forceUpdate = True

		if ( GPIO.input(17)== False ):

			log('Button 4 - Vol Up')
			writeToLCD("Volume", "Up")
			os.system('echo "))))" >> /home/pi/.config/pianobar/ctl')

			forceUpdate = True

		if ( GPIO.input(27)== False ):

			log('Button 5 - Play/Pause')

			if playing_stream == "Playing":
				writeToLCD("Paused", "")
				playing_stream = "Paused"
			else:
				writeToLCD("Playing", "")
				playing_stream = "Playing"

			os.system('echo "p" >> /home/pi/.config/pianobar/ctl')

			forceUpdate = True

		if ( GPIO.input(22)== False ):

			log('Button 6 - Menu')
			
			writeToLCD("Pandora Pi", "Menu")
			sleep(.75)
			menuPg1()

				

		sleep(.25)

		updateLCD(forceUpdate)

def menuPg1():

	writeToLCD("1:Like 2:Dislike", "3:IP 4:Next Pg")

	while GPIO.input(2) == True & GPIO.input(3) == True & GPIO.input(4) == True & GPIO.input(17) == True:

		log("menuPg1: Waiting")

	if ( GPIO.input(2) == False ):

		log('Button 6 - Menu - Sub 1 - Like')
		writeToLCD("Liking", current_song)
		os.system('echo "+" >> /home/pi/.config/pianobar/ctl')

		sleep(2)

		forceUpdate = True

	if ( GPIO.input(3) == False ):

		log('Button 6 - Menu - Sub 2 - DisLike')
		writeToLCD("Disliking", current_song)
		os.system('echo "-" >> /home/pi/.config/pianobar/ctl')

		sleep(2)

		forceUpdate = True

	if ( GPIO.input(4) == False ):

		log('Button 6 - Menu - Sub 3 - IP Address')
		getIPAddress()

		sleep(5)

		forceUpdate = True

	if ( GPIO.input(17) == False ):

		menuPg2()

def menuPg2():

	writeToLCD("1:Prev Pg 2:Cur St", "3:Off 4:Next Pg")

	while GPIO.input(2) == True & GPIO.input(3) == True & GPIO.input(4) == True & GPIO.input(17) == True:

		log("menuPg2: Waiting")

	# if ( GPIO.input(2) == False ):

	# 	log('Button 6 - Menu - Sub 1 - Menu Pg 1')
	# 	menuPg1()

	# if ( GPIO.input(3) == False ):

	# 	log('Button 6 - Menu - Sub 2 - Station Name')
	# 	writeToLCD(current_station_name, "")

	# 	sleep(2)

	# 	forceUpdate = True

	# if ( GPIO.input(4) == False ):

	# 	log('Button 6 - Menu - Sub 3 - Shutdown')
	# 	writeToLCD("Shutting Down", "Thanks")
	# 	os.system('echo "q" >> /home/pi/.config/pianobar/ctl')

	# # if ( GPIO.input(17) == False ):

	# # 	menuPg2()

def log(msg):

	f = open('/home/pi/.config/pianobar/scripts/pandorabox.log', 'a+')
	f.write(msg + '\n')
	f.close()

def updateLCD(fUpdate):

	global forceUpdate
	
	f = open('/home/pi/.config/pianobar/scripts/out', 'r')

	song = f.readline().rstrip()
	
	if fUpdate:
		forceUpdate = False
		parseAndWrite()

	elif current_song != song:
		parseAndWrite()

	f.close()

def parseAndWrite(changedStation = False):

	global current_song
	global current_artist
	global current_station_name

	log("Writing")

	f = open('/home/pi/.config/pianobar/scripts/out', 'r')

	song = f.readline().rstrip()
	artist = f.readline().rstrip()
	station = f.readline().rstrip()

	f.close()

	current_song = song
	current_artist = artist
	current_station_name = station

	if changedStation:
		writeToLCD("Listening To:", station)
	else:
		writeToLCD(song, artist)

def writeToLCD(line1, line2):
	
	global allow_lcd_update

	if len(line1) > 16:
		choppedline1 = line1[0:13] + "..."
	else:
		choppedline1 = line1[0:len(line1)]

	if len(line2) > 16:
		choppedline2 = line2[0:13] + "..."
	else:
		choppedline2 = line2[0:len(line2)]

	if allow_lcd_update:
		
		LCD.open()

		LCD.write('\xFE\x01')
		LCD.write('\xFE\x80')
		LCD.write(choppedline1)
		LCD.write('\xFE\xC0')
		LCD.write(choppedline2)

		LCD.close()

def getIPAddress():

	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(('google.com', 0))
	IPaddr = s.getsockname()[0]

	writeToLCD("IP Address:", IPaddr)

main()