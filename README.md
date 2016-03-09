# freifunk_loopcast
Use Freifunk mesh network to set up infoterminal with chromecast and feed from local client workstation

Based on github.com/balloob/pychromecast from Paulus Schoutsen
makes use of webfs, python, python-tagpy, pip, pychromecast

on ubuntu:
apt-get install webfs python python-tagpy pip

pip install netifaces

pip install pychromecast

be shure to change the friendly name of device - it's hardcoded

local IPv4 is detected - in my case third value is the needed wlan-IP
