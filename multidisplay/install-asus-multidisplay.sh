#!/bin/bash

set -e

mkdir -p ~/.local/logs
mkdir -p ~/.config/autostart

SCRIPT_SRC="asus-multidisplay.py"
SCRIPT_DST="$HOME/.local/bin/asus-multidisplay.py"
DESKTOP_FILE="$HOME/.config/autostart/asus-multidisplay.desktop"
ICON_NAME="input-keyboard"  # You can change this to a custom icon if you have one

# Ensure target directories exist
mkdir -p "$HOME/.local/bin"
mkdir -p "$HOME/.local/share/applications"

# Copy and make executable
cp "$SCRIPT_SRC" "$SCRIPT_DST"
chmod +x "$SCRIPT_DST"

# Create .desktop file
cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Type=Application
Name=ASUS MultiDisplay Monitor
Comment=Monitor ASUS Zenbook keyboard and control display
Exec=python3 $SCRIPT_DST
Icon=$ICON_NAME
Terminal=false
Categories=Utility;
EOF

echo "Installed ASUS MultiDisplay as a GNOME application."
echo "You can now find it in your application launcher."
