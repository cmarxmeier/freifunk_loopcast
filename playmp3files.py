"""
Example that shows how the new Python 2 socket client can be used.
using in combination with local webfs to play out audioclips to chromecast using Freifunk Mesh Network
"""

from __future__ import print_function
import time
import sys
import tagpy
import tagpy.id3v2 as id3v2
import logging
import pychromecast
import pychromecast.controllers.youtube as youtube
from netifaces import interfaces, ifaddresses, AF_INET

id3v2.FrameFactory.instance().setDefaultTextEncoding(tagpy.StringType.UTF8)

def ip4_addresses():
    ip_list = []
    for interface in interfaces():
        for link in ifaddresses(interface)[AF_INET]:
            ip_list.append(link['addr'])
    return ip_list




if '--show-debug' in sys.argv:
    logging.basicConfig(level=logging.DEBUG)


global numclips
numclips=10
global activeclip
activeclip=0
global port
port = '8000'
global mp3path
mp3path ="/srv/ftp/freifunk/music/"

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


url="http://"+wireless+":"+port+"/freifunk/music/freifunk"+str(activeclip)+".mp3"
# get mp3 metadata from file
localname=mp3path+"freifunk"+str(activeclip)+".mp3"
fileref = tagpy.FileRef(localname)
file = fileref.file()
tag = file.ID3v2Tag()

if tag == None:
		# No ID3v2.4.0
		print('No ID3v2.4.0')

if 'APIC' in tag.frameListMap().keys():
               for frame in tag.frameListMap()['APIC']:
                if str(frame.type()) == 'FrontCover':
                        print ("FrontCover gefunden.") 


print (tag.artist)
print (tag.title)
print (tag.album)
print (tag.year)
print (tag.comment)




print("Playing: ", url)
cast.play_media((url), "audio/mpeg")


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
            
	if t > 30 and not cast.media_controller.status.player_state == "PLAYING":
		t = 0

		url = "http://"+wireless+":"+port+"/freifunk/music/freifunk"+str(activeclip)+".mp3"

                # get mp3 metadata from file

	 	localname=mp3path+"freifunk"+str(activeclip)+".mp3"
                fileref = tagpy.FileRef(localname)
                file = fileref.file()
                tag = file.ID3v2Tag()

                if tag == None:
		    # No ID3v2.4.0
		    print('No ID3v2.4.0')

                if 'APIC' in tag.frameListMap().keys():
                   for frame in tag.frameListMap()['APIC']:
                      if str(frame.type()) == 'FrontCover':
                        print ("FrontCover gefunden.") 


                        print (tag.artist)
                        print (tag.title)
                        print (tag.album)
                        print (tag.year)
                        print (tag.comment)
	


	
		print ("Playing: ",url)
		cast.play_media((url), "audio/mpeg")
		activeclip = activeclip + 1

        time.sleep(1)
    except KeyboardInterrupt:
        break

cast.quit_app()
