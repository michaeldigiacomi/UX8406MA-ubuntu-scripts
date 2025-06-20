#!/bin/bash
"""
Setup script for ASUS UX8406MA Keyboard Brightness Control
This script configures user-level permissions so the brightness control
can run without sudo privileges.
"""

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
UDEV_RULES_FILE="99-asus-keyboard.rules"
UDEV_RULES_PATH="/etc/udev/rules.d/${UDEV_RULES_FILE}"

echo -e "${BLUE}ASUS UX8406MA Keyboard Brightness Control Setup${NC}"
echo "=============================================="
echo

# Check if running as root
if [[ $EUID -eq 0 ]]; then
    echo -e "${RED}Error: This script should not be run as root${NC}"
    echo "Please run as a regular user. The script will prompt for sudo when needed."
    exit 1
fi

# Check if the device exists
echo -e "${BLUE}Checking for ASUS UX8406MA device...${NC}"
if lsusb | grep -q "0b05:1b2c"; then
    echo -e "${GREEN}✓ ASUS UX8406MA device found${NC}"
else
    echo -e "${YELLOW}⚠ ASUS UX8406MA device not detected${NC}"
    echo "The device may not be connected or this may not be the correct model."
    echo "Continuing with setup anyway..."
fi
echo

# Check if user is in plugdev group
echo -e "${BLUE}Checking user group membership...${NC}"
if groups "$USER" | grep -q "\bplugdev\b"; then
    echo -e "${GREEN}✓ User $USER is already in plugdev group${NC}"
else
    echo -e "${YELLOW}⚠ User $USER is not in plugdev group${NC}"
    echo "Adding user to plugdev group..."
    sudo usermod -a -G plugdev "$USER"
    echo -e "${GREEN}✓ User added to plugdev group${NC}"
    echo -e "${YELLOW}Note: You may need to log out and back in for group changes to take effect${NC}"
fi
echo

# Install udev rules
echo -e "${BLUE}Installing udev rules...${NC}"
if [[ -f "$SCRIPT_DIR/$UDEV_RULES_FILE" ]]; then
    echo "Installing $UDEV_RULES_FILE to $UDEV_RULES_PATH"
    sudo cp "$SCRIPT_DIR/$UDEV_RULES_FILE" "$UDEV_RULES_PATH"
    sudo chown root:root "$UDEV_RULES_PATH"
    sudo chmod 644 "$UDEV_RULES_PATH"
    echo -e "${GREEN}✓ udev rules installed${NC}"
else
    echo -e "${RED}Error: $UDEV_RULES_FILE not found in $SCRIPT_DIR${NC}"
    exit 1
fi
echo

# Reload udev rules
echo -e "${BLUE}Reloading udev rules...${NC}"
sudo udevadm control --reload-rules
sudo udevadm trigger
echo -e "${GREEN}✓ udev rules reloaded${NC}"
echo

# Install Python dependencies
echo -e "${BLUE}Checking Python dependencies...${NC}"
if python3 -c "import usb.core" 2>/dev/null; then
    echo -e "${GREEN}✓ pyusb is already installed${NC}"
else
    echo "Installing pyusb..."
    if command -v pip3 >/dev/null 2>&1; then
        pip3 install pyusb
    elif command -v apt >/dev/null 2>&1; then
        sudo apt update
        sudo apt install -y python3-usb
    else
        echo -e "${RED}Error: Cannot install pyusb. Please install manually:${NC}"
        echo "  pip3 install pyusb"
        echo "  or"
        echo "  sudo apt install python3-usb"
        exit 1
    fi
    echo -e "${GREEN}✓ pyusb installed${NC}"
fi
echo

# Make script executable
SCRIPT_FILE="keyboard-brightness.py"
if [[ -f "$SCRIPT_DIR/$SCRIPT_FILE" ]]; then
    chmod +x "$SCRIPT_DIR/$SCRIPT_FILE"
    echo -e "${GREEN}✓ Made $SCRIPT_FILE executable${NC}"
elif [[ -f "$SCRIPT_DIR/keboard-brightness.py" ]]; then
    chmod +x "$SCRIPT_DIR/keboard-brightness.py"
    echo -e "${GREEN}✓ Made keboard-brightness.py executable${NC}"
fi
echo

# Test permissions
echo -e "${BLUE}Testing USB device permissions...${NC}"
USB_DEVICE=$(lsusb | grep "0b05:1b2c" | head -1)
if [[ -n "$USB_DEVICE" ]]; then
    BUS=$(echo "$USB_DEVICE" | cut -d' ' -f2)
    DEVICE=$(echo "$USB_DEVICE" | cut -d' ' -f4 | sed 's/://')
    USB_PATH="/dev/bus/usb/$BUS/$DEVICE"
    
    if [[ -r "$USB_PATH" && -w "$USB_PATH" ]]; then
        echo -e "${GREEN}✓ USB device permissions are correct${NC}"
        echo "  Device: $USB_PATH"
        echo "  Permissions: $(ls -la "$USB_PATH")"
    else
        echo -e "${YELLOW}⚠ USB device permissions may not be set correctly${NC}"
        echo "  Device: $USB_PATH"
        echo "  Permissions: $(ls -la "$USB_PATH" 2>/dev/null || echo "Not accessible")"
        echo "You may need to:"
        echo "  1. Unplug and replug the device"
        echo "  2. Log out and back in"
        echo "  3. Restart the system"
    fi
else
    echo -e "${YELLOW}⚠ Cannot test permissions - device not found${NC}"
fi
echo

# Offer to create system-wide symlink
echo -e "${BLUE}System integration options:${NC}"
echo "Would you like to install the script system-wide? (y/N)"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    SYSTEM_SCRIPT_PATH="/usr/local/bin/keyboard-brightness"
    if [[ -f "$SCRIPT_DIR/keyboard-brightness.py" ]]; then
        sudo cp "$SCRIPT_DIR/keyboard-brightness.py" "$SYSTEM_SCRIPT_PATH"
    elif [[ -f "$SCRIPT_DIR/keboard-brightness.py" ]]; then
        sudo cp "$SCRIPT_DIR/keboard-brightness.py" "$SYSTEM_SCRIPT_PATH"
    else
        echo -e "${RED}Error: Script file not found${NC}"
        exit 1
    fi
    sudo chmod +x "$SYSTEM_SCRIPT_PATH"
    echo -e "${GREEN}✓ Script installed to $SYSTEM_SCRIPT_PATH${NC}"
    echo "You can now use: keyboard-brightness <level>"
fi
echo

echo -e "${GREEN}Setup completed successfully!${NC}"
echo
echo -e "${BLUE}Next steps:${NC}"
echo "1. If you were added to the plugdev group, log out and back in"
echo "2. Test the script:"
if [[ -f "/usr/local/bin/keyboard-brightness" ]]; then
    echo "   keyboard-brightness off"
    echo "   keyboard-brightness high"
else
    echo "   ./keyboard-brightness.py off"
    echo "   ./keyboard-brightness.py high"
fi
echo "3. If it still requires sudo, try unplugging and replugging the device"
echo
echo -e "${BLUE}Troubleshooting:${NC}"
echo "- Check device permissions: ls -la /dev/bus/usb/*/* | grep 0b05"
echo "- Verify group membership: groups \$USER"
echo "- Check udev rules: cat $UDEV_RULES_PATH"
echo "- View USB devices: lsusb | grep 0b05"