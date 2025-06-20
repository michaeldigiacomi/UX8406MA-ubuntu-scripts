# ASUS UX8406MA Ubuntu Scripts

A collection of modern utilities and scripts for optimal ASUS UX8406MA (Zenbook Pro 14 OLED) laptop support on Ubuntu with GNOME desktop environment.

## 🚀 Features

- **Keyboard Brightness Control** - Control keyboard backlight with user-level permissions
- **Multi-Display Management** - Automatic secondary display control via GNOME extension
- **Modern Implementation** - Python scripts following Ubuntu GNOME best practices
- **No Sudo Required** - Proper permission management with udev rules
- **Easy Setup** - Automated installation scripts for all components

## 📁 Components

### [Keyboard Brightness Control](./keyboard/brightness/)
Modern Python script to control keyboard backlight brightness levels.

**Features:**
- ✨ No sudo required - runs with user permissions
- 🔧 Support for numeric (0-3) and named levels (off/low/medium/high)
- 🛡️ Safe USB device management with automatic cleanup
- ⚙️ Automated setup script for easy installation

**Quick Start:**
```bash
cd keyboard/brightness/
chmod +x setup.sh
./setup.sh
./keyboard-brightness.py high  # No sudo needed!
```

### [Multi-Display Management](./multidisplay/)
Automatic secondary display control based on keyboard connection status.

Available implementations:
- **[GNOME Extension](./multidisplay/gnome-extension/)** (Recommended) - Native GNOME Shell integration
- **[Desktop Application](./multidisplay/gnome-desktop/)** - Standalone application option

**Features:**
- 🔄 Automatic display toggle when keyboard is connected/disconnected
- 📱 Native GNOME notifications
- 📝 Comprehensive logging
- ⚡ Minimal resource usage

**Quick Start (GNOME Extension):**
```bash
cd multidisplay/gnome-extension/
chmod +x install-extension.sh
./install-extension.sh
gnome-extensions enable asus-multidisplay@ux8406ma
```

## 🔧 System Requirements

- **Hardware:** ASUS UX8406MA (Zenbook Pro 14 OLED)
- **OS:** Ubuntu 20.04+ with GNOME desktop environment
- **Python:** 3.8+
- **Permissions:** User-level (no sudo required after setup)

## 📦 Installation

### Quick Install All Components
```bash
# Clone the repository
git clone https://github.com/mdigiacomi/UX8406MA-ubuntu-scripts.git
cd UX8406MA-ubuntu-scripts

# Install keyboard brightness control
cd keyboard/brightness/
chmod +x setup.sh
./setup.sh

# Install multi-display GNOME extension
cd ../../multidisplay/gnome-extension/
chmod +x install-extension.sh
./install-extension.sh
gnome-extensions enable asus-multidisplay@ux8406ma
```

### Individual Component Installation
Each component has its own installation instructions - see the respective README files.

## 🎯 Ubuntu GNOME Integration

All scripts are designed to integrate seamlessly with Ubuntu GNOME:

- **User-level permissions** using udev rules and plugdev group
- **Native GNOME notifications** for status updates
- **Proper logging** to `~/.local/logs/` directory
- **Desktop integration** with .desktop files and system shortcuts
- **Extension support** for background operation

## 🔍 Usage Examples

### Keyboard Brightness
```bash
# Basic usage
keyboard-brightness off     # Turn off backlight
keyboard-brightness low     # Low brightness
keyboard-brightness medium  # Medium brightness
keyboard-brightness high    # High brightness

# With verbose output
keyboard-brightness --verbose high

# Set up GNOME keyboard shortcuts
# Settings > Keyboard > Custom Shortcuts:
# - Ctrl+Alt+F1: keyboard-brightness off
# - Ctrl+Alt+F2: keyboard-brightness high
```

### Multi-Display (via GNOME Extension)
```bash
# Extension runs automatically in background
# Check status
gnome-extensions list | grep asus-multidisplay

# View logs
tail -f ~/.local/logs/asus-multidisplay-extension.log
```

## 🛠️ Troubleshooting

### Permission Issues
If you encounter permission errors:

1. **Run the setup script:**
   ```bash
   ./setup.sh
   ```

2. **Check group membership:**
   ```bash
   groups $USER
   ```

3. **Verify udev rules:**
   ```bash
   cat /etc/udev/rules.d/99-asus-keyboard.rules
   ```

### Device Detection
If devices aren't detected:

1. **Check USB connections:**
   ```bash
   lsusb | grep 0b05:1b2c  # Keyboard
   lsusb | grep ASUS       # All ASUS devices
   ```

2. **Check system logs:**
   ```bash
   dmesg | grep -i usb | tail -20
   journalctl -f | grep -i asus
   ```

### GNOME Extension Issues
If extensions don't work:

1. **Restart GNOME Shell:**
   ```bash
   # Press Alt+F2, type 'r', press Enter
   # Or log out and back in
   ```

2. **Check extension status:**
   ```bash
   gnome-extensions list --enabled
   ```

## 🔧 Development

### Code Standards
All scripts follow modern Python and Ubuntu best practices:
- Type hints for better documentation
- Context managers for resource management
- Proper error handling and logging
- User-level permissions with udev rules
- GNOME desktop integration

### Contributing
1. Fork the repository
2. Create a feature branch
3. Follow the existing code style
4. Test on Ubuntu GNOME
5. Submit a pull request

### Testing
```bash
# Test keyboard brightness
cd keyboard/brightness/
./keyboard-brightness.py --verbose off
./keyboard-brightness.py --verbose high

# Test multi-display extension
cd multidisplay/gnome-extension/
tail -f ~/.local/logs/asus-multidisplay-extension.log
```

## 📋 Compatibility

- **Tested on:** Ubuntu 22.04 LTS, Ubuntu 24.04 LTS
- **Python versions:** 3.8, 3.9, 3.10, 3.11, 3.12
- **GNOME versions:** 42+
- **Hardware:** ASUS UX8406MA (Zenbook Pro 14 OLED)

## 📄 License

This project is released under the MIT License. See the LICENSE file for details.

## 🆘 Support

For issues, questions, or contributions:

1. **Check the troubleshooting sections** in component READMEs
2. **Search existing issues** on GitHub
3. **Create a new issue** with:
   - Component affected (keyboard/multidisplay)
   - Ubuntu version and GNOME version
   - Error messages and logs
   - Steps to reproduce

## 🎉 Acknowledgments

- Designed specifically for ASUS UX8406MA laptop
- Follows Ubuntu GNOME integration best practices
- Uses modern Python development standards
- Community-driven development and testing

---

**Note:** These scripts are specifically designed for the ASUS UX8406MA laptop model. Other ASUS models may require parameter adjustments.