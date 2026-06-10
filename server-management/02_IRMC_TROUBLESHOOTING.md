# 02: iRMC Interface Access & Legacy Cipher Troubleshooting

Operational guide for overcoming browser access blocks and routing intercept vectors caused by outmoded encryption infrastructure on Fujitsu iRMC S2 integrated management controllers.

## Problem Description

The Fujitsu PRIMERGY TX200 S6 features an integrated Remote Management Controller (iRMC S2) that relies natively on deprecated cryptographic protocols (SSLv3, TLS 1.0, and TLS 1.1) paired with custom self-signed certificates. This triggers two primary access blocks:

1. **Router Interception:** Modern security routers (e.g., TP-Link Deco HomeShield suites) misinterpret the raw legacy handshakes as active malicious browser redirection threats and forcibly display warning blocks or request administrative access to the router app.
2. **Client Browser Rejection:** Modern browsers drop handshakes that fall below minimum TLS 1.2 thresholds, outputting fatal protocol configuration errors.

---

## Resolution Protocols

### Protocol A: Physical Topology Hardening (Router Bypass)

To prevent network security engines from dropping or proxying traffic targeting the management processor, isolate the physical routing layer completely.

1. Interconnect the host desktop's physical LAN interface (`eno1`) directly to the dedicated iRMC port on the server chassis or route them through an unmanaged layer-2 hardware switch isolated from the default gateway router.
2. Force manual host-side routing configuration inside the targeted class (refer to `01_SERVER_DISCOVERY.md`).

### Protocol B: Client Cipher Modification (Firefox Manual Override)

When accessing the web dashboard at the target IP (e.g., `https://192.168.68.249`), the browser must be forced to accept legacy TLS layers.

1. Initialize a new tab within the Firefox web browser and execute the system tuning flag:
```text
about:config

```


2. Acknowledge and bypass the performance configuration warning dialog.
3. Input the target preference configuration path inside the lookup field:
```text
security.tls.version.min

```


4. Modify the integer value from its native default state (`3`, specifying TLS 1.2) to **`1`** (enabling backward compatibility down to TLS 1.0).
5. Navigate explicitly using the direct schema format:
```text
https://[SERVER_iRMC_IP]

```


6. Acknowledge the self-signed untrusted authority certificate exception prompt to gain administrative access to the iRMC console layout.
"""

docs['linux-config/server-management/03_HARDENED_SSH_ACCESS.md'] = """# 03: Hardened SSH Infrastructure

System protocol for shifting server remote administration from vulnerable password-based challenges to hardened key-based asymmetric validation, augmented with target-specific client matching and network firewalls.

---

## Step 1: Client Cryptographic Key Synthesis

Generate a standalone asymmetric key pair on the **host desktop** utilizando standard Ed25519 parameters for high cryptographic performance and structural compactness.

```bash
ssh-keygen -t ed25519 -C "desktop-access"

```

When prompted for path selection, override the standard path parameters to preserve isolation for this explicit server node:

```text
Enter file in which to save the key (/home/george/.ssh/id_ed25519): /home/george/.ssh/fujitsu_access

```

*Leave the passphrase parameters empty if seamless automated scripting is required, or supply an authorization phrase to add local decryption overhead.*

---

## Step 2: Remote Public Key Injection

Transmit the synthesized public key coordinate to the target server operating system instance (e.g., `192.168.68.120`). You must target the specific non-standard public file path:

```bash
ssh-copy-id -i ~/.ssh/fujitsu_access.pub test@192.168.68.120

```

Supply the administrative credentials for the remote account (`test`) to append the cryptographic fingerprint to the server's authorized registry file (`~/.ssh/authorized_keys`).

---

## Step 3: Local Client Profile Optimization

Construct an optimized access definition structure on the **host desktop** to eliminate structural IP and path declarations during connection calls.

1. Instantiate or open the local SSH user config:
```bash
nano ~/.ssh/config

```


2. Integrate the structured execution profile:
```plaintext
Host fujitsu
    HostName 192.168.68.120
    User test
    IdentityFile ~/.ssh/fujitsu_access

```


3. Lock down file system access flags across the local SSH configuration directory to satisfy OpenSSH client constraints:
```bash
chmod 600 ~/.ssh/config
chmod 600 ~/.ssh/fujitsu_access
chmod 644 ~/.ssh/fujitsu_access.pub

```



---

## Step 4: Remote Server Hardening (Daemon Lockdown)

Log into the server and transition the OpenSSH server daemon to a zero-password configuration state, rendering credential-stuffing and automated dictionary passes non-functional.

1. Execute a shell session on the server and modify the central daemon configuration file:
```bash
sudo nano /etc/ssh/sshd_config

```


2. Locate, uncomment, or append the following declaration statements to guarantee uniform configuration matching:
```plaintext
PasswordAuthentication no
KbdInteractiveAuthentication no
PubkeyAuthentication yes

```


3. Test the modified file configuration layout for logical syntax errors before restarting the active process thread:
```bash
sudo sshd -t

```


4. If the check drops no faults, recycle the active daemon thread:
```bash
sudo systemctl restart ssh

```



---

## Step 5: Network Exposure Filtering via Uncomplicated Firewall (UFW)

Enforce layer-4 network limitations directly on the server to restrict port 22 access exclusively to the management desktop host coordinate (`192.168.68.106`), discarding traffic from all other interfaces.

```bash
# Enforce a systemic incoming deny policy
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Authorize explicit, single-host SSH entry
sudo ufw allow from 192.168.68.106 to any port 22 proto tcp

# Initialize the firewall engine
sudo ufw enable
sudo ufw status verbose

```