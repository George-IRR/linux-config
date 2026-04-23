# 11: Docker Management Interfaces

Deployment of graphical and terminal-based monitoring environments for container orchestration.

## Option A: Portainer (Web UI)

Containerized web dashboard running on local ports.

1.  Initialize persistent storage volume:
    ```bash
    docker volume create portainer_data
    ```
2.  Deploy container instance bound to daemon socket:
    ```bash
    docker run -d -p 8000:8000 -p 9443:9443 --name portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce:latest
    ```
3.  Access interface: Navigate browser to `https://localhost:9443`.

## Option B: Lazydocker (Terminal UI)

High-speed terminal dashboard executed natively.

1.  Fetch and execute installation script:
    ```bash
    curl [https://raw.githubusercontent.com/jesseduffield/lazydocker/master/scripts/install_update_linux.sh](https://raw.githubusercontent.com/jesseduffield/lazydocker/master/scripts/install_update_linux.sh) | bash
    ```
2.  Execute interface:
    ```bash
    lazydocker
    ```