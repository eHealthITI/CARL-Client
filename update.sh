#!/bin/bash
exec > /home/pi/carlpi/update_log.txt
exec 2>&1
#Get the cloud's url from .env file
text=$(grep -w CLOUD_URL /home/pi/carlpi/.env | cut -d "=" -f2 |tr -d '\015')
cloud_url=$text
cloud_path="download/carl/client"

download_link="${cloud_url}${cloud_path}"
echo $download_link
#Get user's token from .env file
text=$(grep -w CLOUD_TOKEN /home/pi/carlpi/.env| cut -d "=" -f2 |tr -d '\015')
cloud_token=$text
echo $cloud_token
#creates the full URL
dl="${cloud_url}${cloud_path}"
#Downloads the file from the server using the OAuth Token.
curl --header "Authorization: Token $cloud_token" -H "Content-Type: application/zip" $dl  -o /home/pi/carlpi/latest.zip
echo 'downloaded'
#changes user permissions
chown 1000:1000 /home/pi/carlpi/latest.zip

#gets the name of the folder inside the zip archive
folder=$(unzip -l /home/pi/carlpi/latest.zip |awk  'NR==5 {print $4}'|tr -d '\015')
echo $folder
#unzips its contents
unzip -q -o /home/pi/carlpi/latest.zip "$folder*" 

yes | cp -r $folder*.* .

# rebuild the service with the new source code
sudo docker-compose -f /home/pi/carlpi/docker-compose.yml up -d --build