#!/bin/bash

# #Check current status
 file="conf_status"
 if [ -f "$file" ]
 then
  #Start configuration
 sh sistema_monitoramento/wifi-files/hotspot/conf-hotspot.sh
else
 sh sistema_monitoramento/wifi-files/local_net/conf-wifi.sh
fi

sudo python3 sistema_monitoramento/app/main.py &

