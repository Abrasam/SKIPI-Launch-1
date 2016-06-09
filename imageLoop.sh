#!/bin/bash
while true; do
    String="`date +%s`.jpg"
    echo "Saving to $String"
    fswebcam -r 2048x1536 --no-banner "/home/pi/images/unsent/$String"
    sleep 60s
done

