#!/bin/bash

sudo cp "$DHCPCD_FILE" ./bkup/dhcpcd.conf
sudo cp "$DNS_FILE" ./bkup/dns.conf
sudo cp "$HOSTAPD_FILE" ./bkup/hostapd.conf
sudo cp "$DNS_FILE" ./bkup/dns.conf

#write wifi to wpa_supplicant
cat wifi_append >> /etc/wpa_supplicant/wpa_supplicant.conf

#fix files to enable wifi!
sudo cat "$DHCPCD_APPEND"  > "$DHCPCD_FILE"
sudo cat "$DNS_APPEND" > "$DNS_FILE"
sudo cat "$HOSTAPD_APPEND" >> "$HOSTAPD_FILE"
