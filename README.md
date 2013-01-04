Pandora Pi
============

Python scripts to create the GPIO interface for a Raspberry Pi Pandora Radio streamer.

Build Details
============
You can find full build instructions at my website http://www.shaungehring.com/2013/01/03/raspberry-pi-project-1-pandora-streamer/ . The build will take you through the basic steps of setting up the Pi, using the LCD and buttons and connectng all the code that makes everything run. This is a great first time project only taking a day to put together.


What, do i do???
============
- Get a Raspberry Pi
- Load Pianobar
- Load these scripts
- Connect a 2x16 LCD Display
- Connect 6 tactile buttons
- Connect powered speakers
- Listen to music and control it from the device.

Files
============

Shared.pkl
------------
This is a pickle file used to persist data between the eventReciever and the ButtonWatcher

pandorabox.log
------------
Log file used to record python script output.

ButtonWatcher.py
------------
This script is launched by PandorasBox.sh and runs a loop watching for GPIO input. When it sees a button pressed it then takes the correct action.

eventReciever.py
-------------
This file is a script that is triggered by Pianobar. Pianobar sends this file data when a event is fired. Events include (songstart, songfinish, etc...). When a event happens it saves the relevent data to shared.pkl and updates the Display.

pandoraUtils.py
-------------
Shared utilities to talk to the LCD, write to the Log, Get/Set values in the pickle file.

PandorasBox.sh
-------------
BASH script ran on launch. This script validates that the python scripts only launch if GPIO pin 22 is powered. This is checking that buttons are active to launch.

Whats Needed
============

- Better menu control
- A way to page through stations and not pick a random one (stations are stroed in the pickle file already)
- A way to start and stop Pianobar from the Python script so you can turn the streamer off/on without powering off the Pi.
- Tweet what you are listening to
- Cool Stuff!!!!

Credit
============
Credit goes to AyMac (https://github.com/AyMac/Pandoras-Box) for the first version which was a combination of BASH and Python. This version is a attemp to keep as much in Python as possible. AyMac's original full project can be seen at (http://www.instructables.com/id/Pandoras-Box-An-Internet-Radio-player-made-with/?ALLSTEPS)