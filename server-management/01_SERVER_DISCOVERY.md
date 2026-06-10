# 01: Active and Isolated Network Discovery

Documentation for identifying server IP coordinates across active subnets and unmanaged, non-DHCP switch fabrics.

## Hardware Reference Identifiers
* **iRMC MAC Address:** `00:19:99:C3:87:5A`
* **LAN 1 MAC Address:** `00:19:99:BA:A5:20`
* **Default Factory Hostname:** `IRMCC3875A`

---

## Part 1: Live DHCP Subnet Discovery
When the target server and host desktop are connected to an active router distributing IP configuration parameters via DHCP.

### 1. Subnet Identification
Determine the active operational interface and subnet boundaries on the host machine:

```

```text
All technical documentation modules successfully synthesized and integrated into local workspace.

```bash
ip route show

```

*Example interpretation: `192.168.68.0/24 dev eno1 proto kernel scope link src 192.168.68.106` isolates the target subnet to `192.168.68.0/24` with the host bound to `192.168.68.106`.*

### 2. Accelerated Subnet Scanning

Scan the identified subnet layout using Nmap. The inclusion of the `-n` flag bypasses reverse DNS lookups, mitigating performance hangs caused by network timeouts:

```bash
sudo nmap -sn -n --max-retries 0 192.168.68.0/24 | grep -B 2 -i "00:19:99"

```

The output isolates the active IP address matching the Fujitsu organization vendor block.

---

## Part 2: Isolated Unmanaged Switch Discovery (Non-DHCP Environment)

When the host and server are interconnected exclusively through a layer-2 switch missing an active DHCP server, interfaces drop configurations and default to fallback states.

### 1. Host Interface Initialization

Verify that the host link detects a physical connection (`state UP`, `LOWER_UP` flag active):

```bash
ip link show eno1

```

### 2. Manual IP Allocation (Targeting Factory Defaults)

Fujitsu iRMC modules drop back to a factory default address of `192.168.1.1` when DHCP lease assignments fail. Bind a temporary secondary IP on the host's ethernet adapter to bridge into the `.1.x` subnet:

```bash
sudo ip addr add 192.168.1.200/24 dev eno1

```

*Note: This assignment is volatile, residing strictly in volatile RAM, and will purge automatically upon host system reboot.*

### 3. Execution of Accelerated Factory Segment Search

```bash
sudo nmap -sn -n --max-retries 0 192.168.1.0/24 | grep -B 2 -i "00:19:99:C3:87:5A"

```

### 4. Alternative Link-Local (Auto-IP) Tracing

If the iRMC interface drops into a link-local allocation state (`169.254.x.x`), execute an arbitrary link-local assignment on the host and scan the global B-class network segment:

```bash
sudo ip addr add 169.254.10.10/16 dev eno1
sudo nmap -sn -n --max-retries 0 169.254.0.0/16 | grep -B 2 -i "00:19:99:C3:87:5A"
```