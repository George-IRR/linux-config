# 10: Docker Engine Configuration

Implementation of Docker Community Edition via official repositories and configuration of socket permissions for standard user access.

## Repository Integration and Installation

1.  Install prerequisite transport protocols and cryptographic tools:
    ```bash
    sudo apt update
    sudo apt install ca-certificates curl gnupg
    ```
2.  Establish local keyring and import Docker GPG validation key:
    ```bash
    sudo install -m 0755 -d /etc/apt/keyrings
    curl -fsSL [https://download.docker.com/linux/ubuntu/gpg](https://download.docker.com/linux/ubuntu/gpg) | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    sudo chmod a+r /etc/apt/keyrings/docker.gpg
    ```
3.  Inject repository source map into APT configuration:
    ```bash
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] [https://download.docker.com/linux/ubuntu](https://download.docker.com/linux/ubuntu) \
      $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
      sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    ```
4.  Execute package installation:
    ```bash
    sudo apt update
    sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    ```

## Privilege Escalation Bypass

The Docker daemon binds to a Unix socket owned by the root user. Standard execution without privileges triggers the following failure signature:
`permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock`

Modify system groups to authorize container execution without `sudo`.

1.  Initialize target group:
    ```bash
    sudo groupadd docker
    ```
2.  Append active user:
    ```bash
    sudo usermod -aG docker $USER
    ```
3.  Force group policy refresh for current session:
    ```bash
    newgrp docker
    ```
4.  Verify execution authorization:
    ```bash
    docker ps
    ```