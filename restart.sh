#!/bin/sh
exec > logfile.txt
exec 2>&1

MONITORDIR="/home/pi/carlpi"
inotifywait -m -e create --format '/home/pi/carlpi/reboot' "${MONITORDIR}" | while read NEWFILE
do
	rm -r /home/pi/carlpi/reboot
    echo "a reboot was requested"
    shutdown -r now
done
