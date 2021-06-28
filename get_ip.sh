#!/bin/bash

exec 3>&1 4>&2
trap 'exec 2>&4 1>&3' 0 1 2 3
exec 1>/home/pi/carlpi/deploy_log.txt 2>&1

# Makes sure that nmap is installed
apt --assume-yes install nmap
echo "installed nmap"
# Installs docker and docker-compose
curl -sSL https://get.docker.com | sh
apt --assume-yes install libffi-dev libssl-dev
apt --assume-yes install python3 python3-pip
apt --assume-yes remove python-configparser
sudo pip3 -v install docker-compose
# Installs notify-tools
sudo pip3 -v install python-dotenv


echo "installed docker"
#Finds the IP getaway of the router.
router_ip=$(ip r | awk 'END {print $1}')
echo "found the IP of the router. ($router_ip)"
#Finds the ip of the homecenter lite
fibaro_ip=$(nmap -sP $router_ip | awk '/^Nmap/{ip=$5}/Fibar/{print ip}')
echo "found the ip of HC lite. ($fibaro_ip)"
#Delete the last line the value to .env file
sed -i '/^HC_URL/d' /home/pi/carlpi/.env

#Appends HC_URL key and its value to the .env file
echo 'HC_URL=http://'$fibaro_ip >> /home/pi/carlpi/.env
echo "filled .env file"

# Creates a crontab job to run update.sh script on a daily basis at 7:00AM
crontab -r -u pi
crontab -l -u pi | { cat; echo "0 7 * * * /usr/bin/python3 /home/pi/carlpi/custom_update.py >> /home/pi/carlpi/update_log.txt 2>&1"; } | crontab -u pi -
crontab -l -u pi | { cat; echo "@reboot /home/pi/carlpi/get_ip.sh"; } | crontab -u pi -
echo "set up finished"

docker-compose -f /home/pi/carlpi/docker-compose.yml up -d --build

#remove latest.zip
rm -r /home/pi/carlpi/latest.zip
echo "built!"
