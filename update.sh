
#Get the cloud's url from .env file
text=$(grep -w CLOUD_URL .env | cut -d "=" -f2 |tr -d '\015')
cloud_url=$text
cloud_path="/download/carl/client"

download_link="${cloud_url}${cloud_path}"
#Get user's token from .env file
text=$(grep -w CLOUD_TOKEN .env| cut -d "=" -f2 |tr -d '\015')
cloud_token=$text

dl="${cloud_url}${cloud_path}"

curl --header "Authorization: Token $cloud_token" -H "Content-Type: application/zip" $dl  -o latest.zip


chown 1000:1000 latest.zip
unzip latest.zip