# Investigation Commands

## 1. Check local firewall rules

sudo iptables -L -n -v

## 2. Check route to management server

ip route get <management_server_ip>

## 3. Test TLS connection

timeout 10 openssl s_client -connect <management_server_ip>:<port> -servername <server_fqdn>

## 4. Capture traffic during registration attempt

sudo tcpdump -i <interface> -s0 -nn 'tcp and host <management_server_ip> and port <port> or icmp' -w test-registration.pcap

## 5. Trigger agent registration test

cd /path/to/agent
sudo ./agent test registration /path/to/init-file.dat

## Notes

- Replace placeholder values before running commands.
- Use the correct network interface for the endpoint.
- Capture should run while the registration test is attempted.
- If TCP completes but TLS does not, investigate TLS inspection, proxying, firewall inspection, or other network-path interference.