# Multi-Display Management

Automatic secondary display control for ASUS UX8406MA laptops based on keyboard connection status.

## Overview

This directory contains implementations for automatically managing the secondary display on ASUS UX8406MA laptops. When the detachable keyboard is connected, the secondary display is turned off (laptop mode). When disconnected, the secondary display is enabled (tablet/presentation mode).

## Available Implementations

### [GNOME Extension](./gnome-extension/) (Recommended)
Native GNOME Shell extension that runs seamlessly in the background.

**Advantages:**
- ✨ Native GNOME integration
- 🚀 Auto-starts with GNOME session
- ⚡ Minimal resource usage
- 🔧 Easy management with GNOME tools
- 📱 Native notifications

**Quick Start:**
```bash
cd gnome-extension/
chmod +x install-extension.sh
./install-extension.sh
gnome-extensions enable asus-multidisplay@ux8406ma
```

### Desktop Application (Future Implementation)
Standalone application option for non-GNOME environments or users who prefer traditional applications.

**Features (Planned):**
- 🖥️ System tray integration
- ⚙️ Configuration GUI
- 📋 Cross-desktop compatibility
- 🔄 Manual override controls

## How It Works

1. **Device Detection**: Monitors USB devices using `lsusb` to detect ASUS keyboard presence
2. **Display Control**: Uses `gdctl` (GNOME Display Control) to manage display configuration
3. **State Management**: Tracks keyboard connection state and triggers display changes only on state transitions
4. **Logging**: Comprehensive logging for debugging and monitoring

## Supported Display Configurations

- **Keyboard Connected** (Laptop Mode):
  - Primary display: eDP-1 (main laptop screen)
  - Secondary display: OFF
  
- **Keyboard Disconnected** (Tablet/Presentation Mode):
  - Primary display: eDP-1 (main laptop screen)
  - Secondary display: eDP-2 (positioned right of primary)

## Requirements

### System Requirements
- ASUS UX8406MA laptop with dual displays
- Ubuntu 20.04+ with GNOME desktop environment
- Wayland session (recommended)

### Dependencies
- `lsusb` command (usually pre-installed)
- `gdctl` utility for display management
- GNOME Shell 42+ (for extension)

### Installation of Dependencies
```bash
# Install gdctl if not available
sudo apt update
sudo apt install gnome-display-manager

# Verify lsusb is available
which lsusb
```

## Configuration

The implementations use these default settings:

```javascript
// USB Detection Parameters
VENDOR_ID = "0b05"  // ASUS vendor ID
DEVICE_NAME_KEYWORDS = ["asus", "zenbook", "duo", "keyboard", "primax"]
CHECK_INTERVAL = 2  // seconds between checks

// Display Names (may need adjustment for your setup)
PRIMARY_DISPLAY = "eDP-1"
SECONDARY_DISPLAY = "eDP-2"
```

## Troubleshooting

### Display Names
If the display control doesn't work, check your display names:
```bash
gdctl list
```

### USB Device Detection
Verify your keyboard is detected:
```bash
lsusb | grep -i asus
```

### Permissions
Ensure you have permission to control displays:
```bash
gdctl list  # Should work without sudo
```

## Development

### Adding New Implementations
To add a new implementation (e.g., KDE, XFCE):

1. Create a new subdirectory: `mkdir kde-plasma/`
2. Implement the core logic using appropriate display tools
3. Follow the same monitoring pattern as the GNOME extension
4. Update this README with the new option

### Testing
```bash
# Test display control manually
gdctl set --logical-monitor --monitor eDP-1 --primary
gdctl set --logical-monitor --monitor eDP-1 --primary --logical-monitor --monitor eDP-2 --right-of eDP-1

# Test USB detection
lsusb | grep 0b05
```

## License

MIT License - See the main project LICENSE file for details.

## Compatibility

- **Tested on:** Ubuntu 22.04 LTS, Ubuntu 24.04 LTS
- **GNOME versions:** 42, 43, 44, 45
- **Hardware:** ASUS UX8406MA (Zenbook Pro 14 OLED)

---

**Note:** Display management requires active GNOME/Wayland session. These implementations are specifically designed for the ASUS UX8406MA dual-display configuration.