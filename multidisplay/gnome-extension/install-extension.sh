#!/bin/bash

set -e

EXTENSION_UUID="asus-multidisplay@ux8406ma"
EXTENSION_DIR="$HOME/.local/share/gnome-shell/extensions/$EXTENSION_UUID"
SOURCE_DIR="$(dirname "$0")"

echo "Installing ASUS MultiDisplay GNOME Extension..."

# Create extension directory
mkdir -p "$EXTENSION_DIR"

# Copy extension files
cp "$SOURCE_DIR/metadata.json" "$EXTENSION_DIR/"
cp "$SOURCE_DIR/extension.js" "$EXTENSION_DIR/"

# Create log directory
mkdir -p "$HOME/.local/logs"

echo "Extension installed to: $EXTENSION_DIR"
echo ""
echo "To enable the extension:"
echo "1. Restart GNOME Shell (Alt+F2, type 'r', press Enter)"
echo "   OR log out and log back in"
echo "2. Use GNOME Extensions app or run:"
echo "   gnome-extensions enable $EXTENSION_UUID"
echo ""
echo "To disable the extension:"
echo "   gnome-extensions disable $EXTENSION_UUID"
echo ""
echo "Logs will be written to: ~/.local/logs/asus-multidisplay-extension.log"