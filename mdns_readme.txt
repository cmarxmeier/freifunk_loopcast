If the traffic to the chromecast has to bypass one tunnel,
it will not be found by local host without some help.

vi /etc/avahi/hosts

add an entry with:
<IPv4> friendlyname.local

and copy a friendlyname_chromecast.service to /etc/avahi/services
edit it to match chromecasts friendlyname and contains it uuid

check results of 'avahi-browse -a -r -t'
and 'getent hosts Friendlyname.local'

ping IPv4 of chromecast to get entry into arp-table

