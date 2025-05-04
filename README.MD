# Ansible Playbook: Prometheus Host Metrics Exporter Deployment
https://github.com/Derad6709/kasp.git
## Overview

This Ansible playbook deploys a custom Python-based host metrics exporter compatible with Prometheus. It offers two deployment methods:

1.  **Bare Metal:** Installs the exporter directly on the target host using `pkgx` for Python environment management and `systemd` for service management.
2.  **Docker:** Builds a Docker image containing the exporter and runs it as a container using Docker (installed via `snap`).

The exporter ([`playbook/files/host_metrics_exporter.py`](playbook/files/host_metrics_exporter.py)) collects basic host metrics like CPU usage, memory usage, uptime, and detects the host type (physical, VM, container). Metrics are exposed on port `8080` by default.

## Prerequisites

### Control Node (where you run `ansible-playbook`)

*   Ansible installed.
*   Required Ansible Collections:
    ```bash
    ansible-galaxy collection install community.general community.docker
    ```

### Target Node(s)

*   SSH access configured for Ansible.
*   User with `sudo` privileges (most tasks use `become: true`).
*   Python 3 installed (for Ansible modules).
*   `python3-pip`, `python3-packaging`, `python3-virtualenv` (used by the `ansible.builtin.pip` module, for the Docker role's dependency installation).
*   Internet access (for downloading packages).
*   **For Bare Metal method:** `curl` or `brew` (to install `pkgx`).
*   **For Docker method:** `snapd` service enabled and running (the playbook attempts to install/enable it).

## Configuration

1.  **Inventory:** Define your target hosts in [`inventory.ini`](inventory.ini).
2.  **Playbook Variables:** Global variables are defined in [`playbook/site.yml`](playbook/site.yml).
3.  **Role Defaults:** Role-specific variables can be found and overridden in:
    *   [`playbook/roles/docker_exporter/defaults/main.yml`](playbook/roles/docker_exporter/defaults/main.yml)
    *   Variables for `prometheus_exporter` are primarily set in [`playbook/site.yml`](playbook/site.yml).

## Usage

Run the playbook from the root directory of the project. Use tags to select the desired deployment method.

*   **Deploy using Bare Metal method only:**
    ```bash
    ansible-playbook -i inventory.ini playbook/site.yml --tags bare_metal
    ```

*   **Deploy using Docker method only:**
    ```bash
    ansible-playbook -i inventory.ini playbook/site.yml --tags docker
    ```

*   **Deploy using both methods (on the same host, ports might conflict if defaults aren't changed):**
    ```bash
    ansible-playbook -i inventory.ini playbook/site.yml --tags bare_metal,docker
    # or simply:
    ansible-playbook -i inventory.ini playbook/site.yml
    ```

## Notes

*   The playbook assumes the user running Ansible (`ansible_user` in [`inventory.ini`](inventory.ini)) has passwordless `sudo` privileges on the target hosts, as many tasks require elevation (`become: true`).
*   The default exporter port is `8080`. If running both methods on the same host, ensure you modify the `host_port` variable in [`playbook/roles/docker_exporter/defaults/main.yml`](playbook/roles/docker_exporter/defaults/main.yml) to avoid conflicts.
*   The `docker_exporter` role installs Docker via `snap`. Ensure `snap` is supported on your target system (primarily Debian/Ubuntu derivatives).
*   The `prometheus_exporter` role uses `pkgx` to manage the Python environment, installing it if not found.
