sed -i '/exit 0/i \
iptables-restore < /etc/iptables.ipv4.nat' test1
