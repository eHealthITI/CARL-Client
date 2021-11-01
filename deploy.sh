#!/bin/bash

docker cp carlpi_celery_1:/code/celery.logs /home/pi/carlpi/celery.logs
#got celery.logs from the container
docker exec carlpi_celery_1 sh -c "rm -r /code/celery.logs"
cloud_token=$(cat /home/pi/carlpi/.env | awk -F= '/^CLOUD_TOKEN/ {print $2}')
cloud_url=$(cat /home/pi/carlpi/.env | awk -F= '/^CLOUD_URL/ {print $2}')

#sending celery logs to cloud
curl -s -o /dev/null -X POST -H "Authorization: Token $cloud_token" -H "Content-Type:multipart/form-data" -F "log=@/home/pi/carlpi/celery.logs" $cloud_url/api/device/log/celery

# running get_ip.sh script
. /home/pi/carlpi/get_ip.sh

#Sending the update, deploy logs to cloud
auth_header='Authorization: Token '$cloud_token
curl -s -o /dev/null -X POST -H "Authorization: Token $cloud_token" -H "Content-Type:multipart/form-data" -F "log=@/home/pi/carlpi/deploy_log.txt" $cloud_url/api/device/log/deploy
curl -s -o /dev/null -X POST -H "Authorization: Token $cloud_token" -H "Content-Type:multipart/form-data" -F "log=@/home/pi/carlpi/update_log.txt" $cloud_url/api/device/log/update

