# 06: NFS and mDNS Resolution Recovery over Mesh Networks
Structural analysis of Stale Mount (No such device) errors induced by IP rotation in Mesh networks and permanent remediation via controlled multicast.

## 1. Problem Profile (Thermal / Network Mutation)
In a network topology managed by multiple smart nodes (e.g., TP-Link Deco Mesh), devices can dynamically change their IP address within the same class (e.g., from 192.168.68.112 to 192.168.68.105) following reboots or signal transitions.

If an NFS client (e.g., Raspberry Pi with DietPi) is configured to mount a folder using the local hostname (george-desktop.local), the Mesh network tends to filter IGMP/Multicast discovery packets between Wi-Fi and wired connections. The mDNS service loses consistency, the NFS kernel table freezes in a stale state, and network directories return:
`bash: cd: nfs_client/: No such device`

## 2. Protocol of Emergency Unlocking (Lazy Unmount)
The operating system rejects cd or ls queries on the blocked directory because the kernel waits indefinitely for a response from the old IP. Force immediate detachment from the active mount table:

```bash
sudo umount -f -l /mnt/nfs_client
```
* `-f` (Force): Interrupts pending Read/Write operations in the network.
* `-l` (Lazy): Instantly detaches the directory from the visible filesystem hierarchy, cleaning up locked references in the background.

## 3. Stabilizing mDNS on Systems without systemd-resolved (DietPi/Debian Minimal)
Minimalist distributions strip out complex network packages. To ensure persistence of the .local resolution:

### 1. Forcing Avahi Daemon Execution
Manually install and start the mDNS multicast server on both machines (Server and Client):
```bash
sudo apt update && sudo apt install avahi-daemon -y
sudo systemctl enable --now avahi-daemon
sudo systemctl restart avahi-daemon
```

### 2. Modifying Query Priority in NSSwitch
Tell the operating system to look for the .local suffix using the mDNS multicast driver before sending the failed request to the router's primary DNS.
Open the configuration file:
```bash
sudo nano /etc/nsswitch.conf
```
Modify the `hosts:` line to reflect the exact order:
```text
hosts:          files mdns4_minimal [NOTFOUND=return] dns
```
*Note: The modification is read dynamically by the glibc library; no network manager restart is required.*

## 4. Connection Validation and Remounting the Structure
After configuring Avahi, run the validation steps to confirm alignment:
```bash
# 1. Verify if mDNS intercepts the new IP through the Mesh router
ping -c 3 george-desktop.local

# 2. Query the NFS exports exposed by the desktop
showmount -e george-desktop.local

# 3. Perform the secure mount configured in /etc/fstab
sudo mount /mnt/nfs_client

# 4. List the files
ls -la /mnt/nfs_client
```

## 5. Backup Solution: Static Mapping (Aggressive Router Filtering)
If the router completely blocks Multicast packets in the network and the ping command fails persistently, bypass the network via rigid local mapping:
1. Fix the desktop machine's IP in the router's interface (DHCP Reservation -> 192.168.68.105).
2. Manually add the directive to the Raspberry Pi's local table:
```bash
sudo nano /etc/hosts
```
Insert the line at the end of the file:
```text
192.168.68.105      george-desktop.local
```
