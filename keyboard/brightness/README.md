# ASUS UX8406MA Keyboard Brightness Control

A modern Python script to control keyboard backlight brightness on ASUS UX8406MA laptops running Ubuntu with GNOME desktop environment.

## Features

- ✨ Modern Python implementation with proper error handling
- 🔧 Support for both numeric (0-3) and named brightness levels
- 🛡️ Safe USB device management with automatic cleanup
- 📝 Comprehensive logging and user feedback
- 🎯 Ubuntu GNOME integration ready
- 🔍 Verbose mode for debugging
- 🚀 **No sudo required** - Runs with user-level permissions
- ⚙️ **Easy setup** - Automated permission configuration

## Requirements

### System Requirements
- ASUS UX8406MA laptop
- Ubuntu 20.04+ with GNOME desktop environment
- Python 3.8+
- USB access permissions

### Python Dependencies
```bash
pip install pyusb
```

### System Dependencies
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3-usb libusb-1.0-0-dev

# For development
sudo apt install python3-dev
```

## Installation

### Quick Setup (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mdigiacomi/UX8406MA-ubuntu-scripts.git
   cd UX8406MA-ubuntu-scripts/keyboard/brightness
   ```

2. **Run the automated setup script:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Log out and back in** (if you were added to the plugdev group)

4. **Test the script:**
   ```bash
   ./keyboard-brightness.py high  # No sudo required!
   ```

The setup script will automatically:
- Install required Python dependencies (pyusb)
- Add you to the plugdev group
- Install udev rules for USB permissions
- Test USB device access
- Optionally install the script system-wide

### Manual Installation

If you prefer to set up manually:

1. **Install Python dependencies:**
   ```bash
   pip3 install pyusb
   # Or using apt
   sudo apt install python3-usb
   ```

2. **Add user to plugdev group:**
   ```bash
   sudo usermod -a -G plugdev $USER
   ```

3. **Install udev rules:**
   ```bash
   sudo cp 99-asus-keyboard.rules /etc/udev/rules.d/
   sudo udevadm control --reload-rules
   sudo udevadm trigger
   ```

4. **Log out and back in** for group changes to take effect

5. **Make the script executable:**
   ```bash
   chmod +x keyboard-brightness.py
   ```

## Usage

### Basic Usage

```bash
# Set brightness using numeric levels (0-3)
./keyboard-brightness.py 0    # Turn off backlight
./keyboard-brightness.py 1    # Low brightness
./keyboard-brightness.py 2    # Medium brightness
./keyboard-brightness.py 3    # High brightness

# Set brightness using named levels
./keyboard-brightness.py off     # Turn off backlight
./keyboard-brightness.py low     # Low brightness
./keyboard-brightness.py medium  # Medium brightness
./keyboard-brightness.py high    # High brightness
```

### Advanced Usage

```bash
# Enable verbose output for debugging
./keyboard-brightness.py --verbose high

# Show help and usage information
./keyboard-brightness.py --help

# Show version information
./keyboard-brightness.py --version
```

### Integration Examples

**Create a system-wide command:**
```bash
# Copy to system directory
sudo cp keyboard-brightness.py /usr/local/bin/keyboard-brightness
sudo chmod +x /usr/local/bin/keyboard-brightness

# Now you can use it from anywhere
keyboard-brightness high
```

**Create desktop shortcuts or GNOME shortcuts:**
```bash
# Set keyboard shortcuts in GNOME Settings > Keyboard > Custom Shortcuts
# Command examples:
/usr/local/bin/keyboard-brightness off
/usr/local/bin/keyboard-brightness low
/usr/local/bin/keyboard-brightness medium
/usr/local/bin/keyboard-brightness high
```

## Brightness Levels

| Level | Name   | Description           |
|-------|--------|-----------------------|
| 0     | off    | Backlight turned off  |
| 1     | low    | Low brightness        |
| 2     | medium | Medium brightness     |
| 3     | high   | High brightness       |

## Troubleshooting

### Permission Issues
If you get permission errors:

1. **Check USB permissions:**
   ```bash
   lsusb | grep 0b05:1b2c
   ls -la /dev/bus/usb/*/
   ```

2. **Verify udev rules:**
   ```bash
   cat /etc/udev/rules.d/99-asus-keyboard.rules
   ```

3. **Check group membership:**
   ```bash
   groups $USER
   ```

### Device Not Found
If the script reports "Device not found":

1. **Verify the device is connected:**
   ```bash
   lsusb | grep ASUS
   lsusb | grep 0b05:1b2c
   ```

2. **Check dmesg for USB events:**
   ```bash
   dmesg | grep -i usb | tail -20
   ```

3. **Try with verbose mode:**
   ```bash
   ./keyboard-brightness.py --verbose high
   ```

### USB Communication Errors
If you get USB communication errors:

1. **Run the setup script to fix permissions:**
   ```bash
   ./setup.sh
   ```

2. **Check for conflicting drivers:**
   ```bash
   lsmod | grep usbhid
   ```

3. **Verify the device is accessible:**
   ```bash
   lsusb | grep 0b05:1b2c
   ```

4. **Try unplugging and replugging the device**

5. **As a last resort, try with elevated privileges:**
   ```bash
   sudo ./keyboard-brightness.py high
   ```

## Development

### Running Tests
```bash
# Test basic functionality
./keyboard-brightness.py --verbose off
./keyboard-brightness.py --verbose low
./keyboard-brightness.py --verbose medium
./keyboard-brightness.py --verbose high
```

### Code Style
The project follows modern Python best practices:
- Type hints for better code documentation
- Comprehensive error handling
- Context managers for resource management
- Structured logging
- Clear documentation

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Technical Details

### USB Communication
- **Vendor ID:** 0x0b05 (ASUS)
- **Product ID:** 0x1b2c (UX8406MA keyboard)
- **Interface:** 4
- **Report ID:** 0x5A
- **Communication:** HID SET_REPORT control transfer

### Data Packet Structure
```
Byte 0: Report ID (0x5A)
Byte 1: 0xBA
Byte 2: 0xC5
Byte 3: 0xC4
Byte 4: Brightness level (0-3)
Bytes 5-15: Padding (0x00)
```

## License

This project is released under the MIT License. See the LICENSE file for details.

## Compatibility

- **Tested on:** Ubuntu 22.04 LTS, Ubuntu 24.04 LTS
- **Python versions:** 3.8, 3.9, 3.10, 3.11, 3.12
- **Hardware:** ASUS UX8406MA (Zenbook Pro 14 OLED)

## Changelog

### Version 2.0
- Complete rewrite with modern Python practices
- Added named brightness levels (off/low/medium/high)
- Improved error handling and logging
- Added context manager for USB device management
- Enhanced command-line interface
- Better Ubuntu GNOME integration
- **User-level permissions** - No sudo required
- **Automated setup script** for easy installation

### Version 1.0
- Initial basic implementation
- Numeric brightness levels only
- Basic USB communication
- Required sudo privileges

## Support

For issues, questions, or contributions, please:
1. Check the troubleshooting section above
2. Search existing issues on GitHub
3. Create a new issue with detailed information

---

**Note:** This script is specifically designed for the ASUS UX8406MA laptop model. Other ASUS models may require different USB parameters.