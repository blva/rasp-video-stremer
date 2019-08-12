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
cat "$DHCPCD_APPEND"  >> "$DHCPCD_FILE"
#Restart DHPCD
sudo service dhcpcd restart
#Configure DHCP server
if [ ! -f "$DNS_ORIGINAL"]; then
    sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
    cat "$DNS_APPEND" >> "$DNS_FILE"
else
    cat "$DNS_APPEND" > "$DNS_FILE"
fi
#Reload DNS
sudo systemctl reload dnsmasq
#Configure Access Point
    cat "$HOSTAPD_APPEND" >> "$HOSTAPD_FILE"
#Inform configuration path
sed -i '/DAEMON_CONF=/c\DAEMON_CONF="/etc/hostapd/hostapd.conf"' /etc/default/hostapd
#Enable hostapd
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl start hostapd
#Add route and masks
sed -i '/#net.ipv4.ip_forward=1/c\net.ipv4.ip_forward=1' /etc/sysctl.conf
sudo iptables -t nat -A  POSTROUTING -o eth0 -j MASQUERADE
sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"
#Write above exit 0
sed -i '/exit 0/i \
iptables-restore < /etc/iptables.ipv4.nat' /etc/rc.local
#Reboot
sudo reboot



