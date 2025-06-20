#!/usr/bin/env python3
"""
ASUS UX8406MA Keyboard Brightness Control

A modern Python script to control keyboard brightness on ASUS UX8406MA laptops
running Ubuntu with GNOME desktop environment.
"""

import argparse
import logging
import sys
import contextlib
from typing import Optional
import usb.core
import usb.util

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# USB Device Configuration
class USBConfig:
    """USB device configuration constants"""
    VENDOR_ID = 0x0b05
    PRODUCT_ID = 0x1b2c
    REPORT_ID = 0x5A
    WVALUE = 0x035A
    WINDEX = 4
    WLENGTH = 16
    TIMEOUT = 1000

# Brightness levels
BRIGHTNESS_LEVELS = {
    'off': 0,
    'low': 1,
    'medium': 2,
    'high': 3
}

def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments with improved user experience"""
    parser = argparse.ArgumentParser(
        description='Control ASUS UX8406MA keyboard brightness',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Brightness levels:
  0, off     - Turn off keyboard backlight
  1, low     - Low brightness
  2, medium  - Medium brightness  
  3, high    - High brightness

Examples:
  %(prog)s 2        # Set to medium brightness
  %(prog)s high     # Set to high brightness
  %(prog)s off      # Turn off backlight
        """
    )
    
    parser.add_argument(
        'level',
        help='Brightness level (0-3 or off/low/medium/high)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 2.0'
    )
    
    return parser.parse_args()

def validate_brightness_level(level_input: str) -> int:
    """
    Validate and convert brightness level input to integer
    
    Args:
        level_input: User input for brightness level
        
    Returns:
        Integer brightness level (0-3)
        
    Raises:
        ValueError: If input is invalid
    """
    # Try to parse as integer first
    try:
        level = int(level_input)
        if 0 <= level <= 3:
            return level
        raise ValueError(f"Numeric level must be between 0 and 3, got {level}")
    except ValueError:
        pass
    
    # Try to parse as named level
    level_input = level_input.lower()
    if level_input in BRIGHTNESS_LEVELS:
        return BRIGHTNESS_LEVELS[level_input]
    
    valid_options = list(BRIGHTNESS_LEVELS.keys()) + ['0', '1', '2', '3']
    raise ValueError(f"Invalid brightness level '{level_input}'. Valid options: {', '.join(valid_options)}")

@contextlib.contextmanager
def usb_device_context(vendor_id: int, product_id: int, interface: int):
    """
    Context manager for USB device operations with proper cleanup
    
    Args:
        vendor_id: USB vendor ID
        product_id: USB product ID  
        interface: USB interface number
        
    Yields:
        usb.core.Device: USB device object
        
    Raises:
        RuntimeError: If device cannot be found or configured
    """
    dev = usb.core.find(idVendor=vendor_id, idProduct=product_id)
    
    if dev is None:
        error_msg = f"Device not found (Vendor ID: 0x{vendor_id:04X}, Product ID: 0x{product_id:04X})\n"
        error_msg += "Troubleshooting steps:\n"
        error_msg += "1. Verify device is connected: lsusb | grep 0b05:1b2c\n"
        error_msg += "2. Run the setup script: ./setup.sh\n"
        error_msg += "3. Check USB permissions in /dev/bus/usb/"
        raise RuntimeError(error_msg)
    
    # Track if we detached the kernel driver
    detached_driver = False
    
    try:
        # Detach kernel driver if necessary
        if dev.is_kernel_driver_active(interface):
            dev.detach_kernel_driver(interface)
            detached_driver = True
            logger.debug(f"Detached kernel driver from interface {interface}")
        
        # Claim the interface
        usb.util.claim_interface(dev, interface)
        logger.debug(f"Claimed USB interface {interface}")
        
        yield dev
        
    except usb.core.USBError as e:
        error_code = getattr(e, 'errno', None)
        if error_code == 13 or 'Permission denied' in str(e) or 'Access denied' in str(e):
            error_msg = f"Permission denied accessing USB device.\n"
            error_msg += "This usually means USB permissions are not set up correctly.\n"
            error_msg += "Try running: ./setup.sh\n"
            error_msg += "Or check if you're in the 'plugdev' group: groups $USER\n"
            error_msg += f"Original error: {e}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)
        else:
            logger.error(f"USB operation failed: {e}")
            raise RuntimeError(f"USB device operation failed: {e}")
    finally:
        # Clean up: release interface and reattach driver
        try:
            usb.util.release_interface(dev, interface)
            logger.debug(f"Released USB interface {interface}")
        except usb.core.USBError:
            logger.warning("Failed to release USB interface")
        
        if detached_driver:
            try:
                dev.attach_kernel_driver(interface)
                logger.debug(f"Reattached kernel driver to interface {interface}")
            except usb.core.USBError:
                logger.warning("Failed to reattach kernel driver")

def set_keyboard_brightness(level: int) -> None:
    """
    Set the keyboard brightness level
    
    Args:
        level: Brightness level (0-3)
        
    Raises:
        RuntimeError: If USB communication fails
        ValueError: If brightness level is invalid
    """
    if not 0 <= level <= 3:
        raise ValueError(f"Brightness level must be between 0 and 3, got {level}")
    
    logger.info(f"Setting keyboard brightness to level {level}")
    
    # Prepare the data packet
    data = [0] * USBConfig.WLENGTH
    data[0] = USBConfig.REPORT_ID
    data[1] = 0xBA
    data[2] = 0xC5
    data[3] = 0xC4
    data[4] = level
    
    try:
        with usb_device_context(USBConfig.VENDOR_ID, USBConfig.PRODUCT_ID, USBConfig.WINDEX) as dev:
            # Send the control transfer
            bm_request_type = 0x21  # Host to Device | Class | Interface
            b_request = 0x09        # SET_REPORT
            
            ret = dev.ctrl_transfer(
                bm_request_type,
                b_request, 
                USBConfig.WVALUE,
                USBConfig.WINDEX,
                data,
                timeout=USBConfig.TIMEOUT
            )
            
            if ret != USBConfig.WLENGTH:
                logger.warning(f"Only {ret} bytes sent out of {USBConfig.WLENGTH}")
            else:
                logger.info("Keyboard brightness set successfully")
                
    except RuntimeError as e:
        logger.error(f"Failed to set keyboard brightness: {e}")
        raise

def main() -> None:
    """Main entry point"""
    try:
        args = parse_arguments()
        
        # Configure logging level based on verbose flag
        if args.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
            logger.debug("Verbose logging enabled")
        
        # Validate and convert brightness level
        brightness_level = validate_brightness_level(args.level)
        
        # Set the keyboard brightness
        set_keyboard_brightness(brightness_level)
        
    except ValueError as e:
        logger.error(f"Invalid input: {e}")
        sys.exit(1)
    except RuntimeError as e:
        logger.error(f"Operation failed: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
