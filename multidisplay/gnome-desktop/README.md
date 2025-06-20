# ASUS MultiDisplay Monitor

This utility monitors the presence of the ASUS Zenbook keyboard (or similar devices) and automatically toggles the secondary display using GNOME/Wayland tools.

## Features

- Detects keyboard connection/disconnection via `lsusb`
- Automatically enables/disables the secondary display
- Logs events to `~/.local/logs/asus-multidisplay.log`
- Installs as a GNOME application for easy launching

## Installation

1. **Clone or copy this repository.**
2. **Run the install script:**
   ```bash
   ./install-asus-multidisplay.sh
   ```
   This will:
   - Copy the script to `~/.local/bin/`
   - Create a GNOME `.desktop` launcher

3. **(Optional) Add a custom icon:**
   - Place your icon (e.g., `asus.png`) in `~/.local/share/icons/` and edit the `.desktop` file to use it.

## Usage

- Launch "ASUS MultiDisplay Monitor" from your GNOME application menu.
- The script will run in a terminal and monitor the keyboard connection status.
- Logs are written to `~/.local/logs/asus-multidisplay.log`.

## Uninstallation

Remove the following files:
- `~/.local/bin/asus-multidisplay`
- `~/.local/share/applications/asus-multidisplay.desktop`
- (Optional) `~/.local/logs/asus-multidisplay.log`

## Requirements

- Python 3
- GNOME/Wayland session
- `gdctl` utility installed and available in PATH

## License

MIT License