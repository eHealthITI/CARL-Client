#!/bin/bash

exec > logfile.txt
exec 2>&1
# Builds the docker images 
docker-compose build -d
echo "FINISHED BUILDING"
echo "STARTING!!!!!" 
# Creates and starts the docker containers 
docker-compose up -d





