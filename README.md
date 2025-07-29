# UniFi CLI Tool

A command-line interface (CLI) tool to manage UniFi Network devices, clients, sites, and hotspot vouchers.

## Features

- List and manage UniFi sites.
- List, get details, restart devices, and power cycle ports on UniFi devices.
- List and get details of connected clients.
- Generate, list, and delete Hotspot vouchers.
- Get UniFi Network application information.
- Supports filtering for list commands.
- Configuration via `~/.unifi_cli.json` or environment variables.

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/haasonsaas/unifi-cli.git
    cd unifi-cli
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the tool in editable mode:**

    ```bash
    pip install -e .
    ```

## Configuration

Create a file named `.unifi_cli.json` in your home directory (`~/.unifi_cli.json`) with your UniFi controller URL and API key:

```json
{
    "url": "https://your-unifi-controller-ip:8443",
    "api_key": "YOUR_API_KEY"
}
```

Alternatively, you can set the `UNIFI_URL` and `UNIFI_API_KEY` environment variables.

## Usage

To see all available commands:

```bash
unifi --help
```

Examples:

-   **List sites:**

    ```bash
    unifi sites list
    ```

-   **List devices for a site:**

    ```bash
    unifi devices list --site-id <site-id>
    ```

-   **Restart a device:**

    ```bash
    unifi devices restart --site-id <site-id> --device-id <device-id>
    ```

-   **Generate a hotspot voucher:**

    ```bash
    unifi hotspot vouchers generate --site-id <site-id> --name "Guest Voucher" --time-limit 60
    ```
