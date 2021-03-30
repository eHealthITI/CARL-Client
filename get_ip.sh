#!/bin/bash

exec > /home/pi/carlpi/logfile.txt
exec 2>&1

# Makes sure that nmap is installed
apt --assume-yes install nmap
echo "installed nmap"
# Installs docker and docker-compose
curl -sSL https://get.docker.com | sh
apt --assume-yes install libffi-dev libssl-dev
apt --assume-yes install python3 python3-pip
apt --assume-yes remove python-configparser
sudo pip3 -v install docker-compose


echo "installed docker"
#Finds the IP getaway of the router.
router_ip=$(ip r | awk 'END {print $1}')
echo "found the IP of the router. ($router_ip)"
#Finds the ip of the homecenter lite
fibaro_ip=$(nmap -sP $router_ip | awk '/^Nmap/{ip=$5}/Fibar/{print ip}')
echo"found the ip of HC lite. ($fibaro_ip)"
#Delete the last line the value to .env file
sed -i '/^HC_URL/d' /home/pi/carlpi/.env

#Appends HC_URL key and its value to the .env file
echo 'HC_URL='$fibaro_ip >> /home/pi/carlpi/.env


# Creates a crontab job to run update.sh script on a daily basis at 7:00AM
cronrab -r 
crontab -l | { cat; echo "0 7 * * * /home/pi/carlpi/update.sh"; } | crontab -

echo "filled .env file"

docker-compose -f /home/pi/carlpi/docker-compose.yml up --build