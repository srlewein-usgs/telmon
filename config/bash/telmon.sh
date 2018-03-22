#!/bin/sh

# Watch the telemetry incoming directory. Uses linux inotifywait tool
# to receive notification that a new file has been created in the directory.
#
# When the file is created, the file is passed to the telmon program for 
# processing to a database
#
# Usage: telmon.sh
#           $1 Directory to monitor (Add trailing slash to path eg. /usr/tmp/)
#           $2 Database connection string
#           $3 Database user
#           $4 Database pwd
#
# It is anticipated that this file will be run as a linux service, though
# it can certainly be run manually

if [ "$#" -ne 1 ] && [ "$#" -ne 4 ]; then
    echo "Usage: $0 cmd 'directory to monitor' (Add trailing slash to path eg. /usr/tmp/) 'DB Connection String' 'User name' 'Password'"
    exit 1;
fi

DIR_TO_WATCH=$1

if [ "$#" -ne 4 ]; then
    DB_CONNECT=$2
	USER=$3
	PWD=$4
fi

inotifywait -m -e create --format "%f" "$DIR_TO_WATCH" | while read NEWFILE
do
        UPFILE=$1$NEWFILE
        echo "processing ${UPFILE}" 
        python3 ../../telmon/parseEDL.py -f $UPFILE
done