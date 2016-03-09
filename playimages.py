"""
Example that shows how the new Python 2 socket client can be used.
using in combination with local webfs to play out image-sequence to chromecast using Freifunk Mesh Network
"""

from __future__ import print_function
import time
import sys
import logging
import pychromecast
import pychromecast.controllers.youtube as youtube
from netifaces import interfaces, ifaddresses, AF_INET

def ip4_addresses():
    ip_list = []
    for interface in interfaces():
        for link in ifaddresses(interface)[AF_INET]:
            ip_list.append(link['addr'])
    return ip_list




if '--show-debug' in sys.argv:
    logging.basicConfig(level=logging.DEBUG)


global numclips
numclips=7
global activeclip
activeclip=0
global port
port = '8000'

myadresses=ip4_addresses()

print ("IP-Adressen lokal: ",myadresses)

# hard coded - TODO - check for the one with 10.xxx.xxx.xxx
wireless = myadresses[2]

print ("My wireless IP: ", wireless)

# Chromecasts
#  MAC			friendly name
#
# 6C:AD:F8:B1:57:01	Freifunk Chromecast 01
#


cast = pychromecast.get_chromecast("Freifunk Chromecast 01")
yt = youtube.YouTubeController()
cast.register_handler(yt)
cast.wait()

print()
print(cast.device)
time.sleep(1)
print()
print(cast.status)
print()
print(cast.media_controller.status)
print()

if '--show-status-only' in sys.argv:
    sys.exit()

if not cast.is_idle:
    print("Killing current running app")
    cast.quit_app()
    time.sleep(5)


url="http://"+wireless+":"+port+"/freifunk/images/freifunk"+str(activeclip)+".jpg"
print("Playing: ", url)
cast.play_media((url), "image/jpg")


t = 0
activeclip = 1

while True:
    try:
        t += 1
 
	if activeclip > numclips:
		activeclip = 1
	
        if t > 10 and t % 3 == 0:
         
	   print("Media status", cast.media_controller.status)

#	   print("Player state", cast.media_controller.status.player_state)
            
	if t > 20 and not cast.media_controller.status.player_state == "PLAYING":
		t = 0

		url = "http://"+wireless+":"+port+"/freifunk/images/freifunk"+str(activeclip)+".jpg"
		print ("Playing: ",url)
		cast.play_media((url), "image/jpg")
		activeclip = activeclip + 1

        time.sleep(1)
    except KeyboardInterrupt:
        break

cast.quit_app()
