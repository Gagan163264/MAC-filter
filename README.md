# [MAC-filter](https://github.com/Gagan163264/MAC-filter)
MAC whitelist filter running on a Raspberry Pi with Pi-Hole(DNS sinkhole)
## Setup
Download files using

`git clone https://github.com/Gagan163264/MAC-filter`

Set permissions for `install.sh` using `chmod +x install.sh` to allow execution and run it. This will install Flash and APScheduler

Run the program with `python main.py`

Place a logo.png file in static/img and replace 'Title' with required text

## Use
Used as a paid service to whitelist given MACs by modifying the `/etc/dnsmasq.d/03-custom-DHCP.conf` file in Pi-Hole so only these MAC id's can access DNS responses.

Whitelisting is done with a web interface where MACs tied to a phone number can be added, deleted or modified.MAC IDs that cross the due date will be auto deleted

To add new users for the website run `python auth.py`(access allowed only to system admins)
