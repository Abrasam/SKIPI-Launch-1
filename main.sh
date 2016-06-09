#!/bin/bash
echo "===================="
python setAirborneGPS.py
echo "===================="
while true; do
        ID="`head -n 1 count.txt`"
        python increment.py
        Var="`find ~/images/unsent -printf '%s %p\n'|sort -nr|head -n 1`"
        String=${Var#*unsent/}
        echo $String
        convert -resize 128x96 "/home/pi/images/unsent/$String" /home/pi/images$
        ./ssdv -e -c SKIPI -i "$ID"  /home/pi/images/temp/temp.jpg output.bin
        python sendImage.py
        mv "/home/pi/images/unsent/$String" "/home/pi/images/sent/$String"
        sleep 0.5
done
