#!/bin/bash

#Install Dependencies
sudo apt install dnsmasq hostapd
sudo systemctl stop dnsmasq
sudo systemctl stop hostapd

#Files that will be updated
DHCPCD_FILE=/etc/dhcpcd.conf
DHCPCD_APPEND=./dhcpcd_append
DNS_APPEND=./dns_append
DNS_FILE=/etc/dnsmasq.conf
DNS_ORIGINAL=/etc/dnsmasq.conf.orig
HOSTAPD_FILE=/etc/hostapd/hostapd.conf
HOSTAPD_APPEND=./hostapd_append
#Update DHPCD file
sudo cat "$DHCPCD_APPEND"  > "$DHCPCD_FILE"
#Restart DHPCD
sudo service dhcpcd restart
sudo systemctl daemon-reload
#Configure DHCP server
sudo cat "$DNS_APPEND" > "$DNS_FILE"
#Reload DNS
sudo systemctl reload dnsmasq
#Configure Access Point
    sudo cat "$HOSTAPD_APPEND" > "$HOSTAPD_FILE"
#Inform configuration path
sudo sed -i '/DAEMON_CONF=/c\DAEMON_CONF="/etc/hostapd/hostapd.conf"' /etc/default/hostapd
#Enable hostapd
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl start hostapd
#Show status
sudo systemctl status hostapd
sudo systemctl status dnsmasq
#Add route and masks
sudo sed -i '/#net.ipv4.ip_forward=1/c\net.ipv4.ip_forward=1' /etc/sysctl.conf
sudo iptables -t nat -A  POSTROUTING -o eth0 -j MASQUERADE
sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"
#Write above exit 0
sudo sed -i '/exit 0/i \
iptables-restore < /etc/iptables.ipv4.nat' /etc/rc.local
#Reboot
sudo reboot



