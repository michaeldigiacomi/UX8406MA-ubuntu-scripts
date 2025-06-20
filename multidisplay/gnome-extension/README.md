# ASUS MultiDisplay GNOME Extension

This GNOME Shell extension monitors the presence of the ASUS Zenbook keyboard and automatically toggles the secondary display using GNOME/Wayland tools. It runs seamlessly in the background as part of GNOME Shell.

## Features

- Runs as a native GNOME Shell extension (no separate processes)
- Detects keyboard connection/disconnection via `lsusb`
- Automatically enables/disables the secondary display
- Logs events to `~/.local/logs/asus-multidisplay-extension.log`
- Shows notifications when keyboard state changes
- Minimal resource usage with efficient polling

## Installation

1. **Navigate to the extension directory:**
   ```bash
   cd gnome-extension
   ```

2. **Run the install script:**
   ```bash
   chmod +x install-extension.sh
   ./install-extension.sh
   ```

3. **Enable the extension:**
   ```bash
   # Restart GNOME Shell first
   # Press Alt+F2, type 'r', press Enter
   # OR log out and log back in
   
   # Then enable the extension
   gnome-extensions enable asus-multidisplay@ux8406ma
   ```

## Usage

- Once enabled, the extension runs automatically in the background
- It will show a notification when first enabled
- Keyboard connection/disconnection events are logged
- The extension will automatically start when you log in to GNOME

## Management

**Check extension status:**
```bash
gnome-extensions list | grep asus-multidisplay
```

**Enable extension:**
```bash
gnome-extensions enable asus-multidisplay@ux8406ma
```

**Disable extension:**
```bash
gnome-extensions disable asus-multidisplay@ux8406ma
```

**View logs:**
```bash
tail -f ~/.local/logs/asus-multidisplay-extension.log
```

## Uninstallation

```bash
# Disable the extension
gnome-extensions disable asus-multidisplay@ux8406ma

# Remove extension files
rm -rf ~/.local/share/gnome-shell/extensions/asus-multidisplay@ux8406ma

# (Optional) Remove logs
rm ~/.local/logs/asus-multidisplay-extension.log
```

## Requirements

- GNOME Shell 42+ (supports older versions back to 42)
- GNOME/Wayland session
- `gdctl` utility installed and available in PATH
- `lsusb` command available

## Advantages over Desktop Application

- **Native Integration**: Runs as part of GNOME Shell, no separate process
- **Auto-start**: Automatically starts with GNOME session
- **Resource Efficient**: Uses GNOME's event loop, minimal overhead
- **No Terminal**: Runs silently in background without terminal windows
- **System Integration**: Proper GNOME notifications and logging
- **Easy Management**: Use standard GNOME extension tools

## Troubleshooting

If the extension doesn't work:

1. **Check if it's enabled:**
   ```bash
   gnome-extensions list --enabled | grep asus-multidisplay
   ```

2. **Check GNOME Shell logs:**
   ```bash
   journalctl -f -o cat /usr/bin/gnome-shell
   ```

3. **Restart GNOME Shell:**
   - Press Alt+F2, type 'r', press Enter
   - Or log out and log back in

4. **Check extension logs:**
   ```bash
   tail -f ~/.local/logs/asus-multidisplay-extension.log
   ```

## License

MIT License