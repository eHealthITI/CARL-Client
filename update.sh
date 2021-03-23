
#Get the cloud's url from .env file
text=$(grep -w CLOUD_URL .env | cut -d "=" -f2 |tr -d '\015')
cloud_url=$text
cloud_path="/download/carl/client"

download_link="${cloud_url}${cloud_path}"
#Get user's token from .env file
text=$(grep -w CLOUD_TOKEN .env| cut -d "=" -f2 |tr -d '\015')
cloud_token=$text
#creates the full URL
dl="${cloud_url}${cloud_path}"
#Downloads the file from the server using the OAuth Token.
curl --header "Authorization: Token $cloud_token" -H "Content-Type: application/zip" $dl  -o latest.zip

#changes user permissions
chown 1000:1000 latest.zip

#gets the name of the folder inside the zip archive
folder=$(unzip -l latest.zip |awk  'NR==5 {print $4}'|tr -d '\015')
echo $folder
#unzips its contents
unzip -q -o latest.zip "$folder*" 

yes | cp -r $folder*.* .

# rebuild the service with the new source code
docker-compose up -d --build