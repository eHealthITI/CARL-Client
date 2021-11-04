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
sudo wget http://ftp.us.debian.org/debian/pool/main/libs/libseccomp/libseccomp2_2.5.1-1_armhf.deb
sudo sudo dpkg -i libseccomp2_2.5.1-1_armhf.deb


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

cloud_token=$(cat /home/pi/carlpi/.env | awk -F= '/^CLOUD_TOKEN/ {print $2}')
cloud_url=$(cat /home/pi/carlpi/.env | awk -F= '/^CLOUD_URL/ {print $2}')


#### Sending logs ####

## Gets celery logs that is stored in the container
docker cp carlpi_celery_1:/code/celery.logs /home/pi/carlpi/celery.logs

## Delete the celery logs insided the container to minimize the size 
docker exec carlpi_celery_1 sh -c "rm -r /code/celery.logs"

## Sending celery logs to cloud
curl -s -o /dev/null -X POST -H "Authorization: Token $cloud_token" -H "Content-Type:multipart/form-data" -F "log=@/home/pi/carlpi/celery.logs" $cloud_url/api/device/log/celery

# Sending update logs 
curl -s -o /dev/null -X POST -H "Authorization: Token $cloud_token" -H "Content-Type:multipart/form-data" -F "log=@/home/pi/carlpi/update_log.txt" $cloud_url/api/device/log/update

docker-compose -f /home/pi/carlpi/docker-compose.yml up -d --build

#remove latest.zip
rm -r /home/pi/carlpi/latest.zip
echo "built!"
# Moves the output to a dummy file. This is done so the that the next command works
exec 1>/home/pi/carlpi/deploy_dump.txt 2>&1

## Sending Deploy Logs.
curl -s -o /dev/null -X POST -H "Authorization: Token $cloud_token" -H "Content-Type:multipart/form-data" -F "log=@/home/pi/carlpi/deploy_log.txt" $cloud_url/api/device/log/deploy