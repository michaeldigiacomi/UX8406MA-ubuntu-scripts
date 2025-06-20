import subprocess
import os
import logging
import time

VENDOR_ID = "0b05"
DEVICE_NAME_KEYWORDS = {"asus", "zenbook", "duo", "keyboard", "primax"}  # use set for O(1) lookup

# Ensure log directory exists
LOG_DIR = os.path.expanduser("~/.local/logs/")
LOG_FILE = os.path.join(LOG_DIR, "asus-multidisplay.log")
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE)
    ]
)

def is_wayland() -> bool:
    return os.environ.get('XDG_SESSION_TYPE') == 'wayland' or os.environ.get('WAYLAND_DISPLAY') is not None

def control_display_1(turn_on: bool = True) -> None:
    try:
        if turn_on:
            commands = [
                [
                    'gdctl', 'set',
                    '--logical-monitor', '--monitor', 'eDP-1', '--primary',
                    '--logical-monitor', '--monitor', 'eDP-2', '--right-of', 'eDP-1'
                ],
            ]
            logging.info("Turning ON display 1 (Wayland)")
        else:
            commands = [
                ['gdctl', 'set', '--logical-monitor', '--monitor', 'eDP-1', '--primary'],
            ]
            logging.info("Turning OFF display 1 (Wayland)")
        success = False
        for cmd in commands:
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    logging.info(f"Success with command: {' '.join(cmd)}")
                    success = True
                    break
                else:
                    logging.warning(f"Command failed: {' '.join(cmd)} - {result.stderr.strip()}")
            except (subprocess.TimeoutExpired, FileNotFoundError) as e:
                logging.warning(f"Command not found or timeout: {' '.join(cmd)} - {e}")
                continue
        if not success:
            logging.warning("No working Wayland display manager found.")
    except Exception as e:
        logging.error(f"Error controlling display: {e}")

def run_lsusb() -> str:
    try:
        result = subprocess.run(['lsusb'], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        logging.error(f"Error running lsusb: {e}")
        return ""

def keyboard_present(lsusb_output: str) -> bool:
    for line in lsusb_output.splitlines():
        lower_line = line.lower()
        if VENDOR_ID in lower_line:
            # Only check keywords if vendor ID matches
            if any(keyword in lower_line for keyword in DEVICE_NAME_KEYWORDS):
                return True
    return False

def monitor_keyboard(interval: float = 1.0) -> None:  # less frequent polling
    logging.info("Monitoring for keyboard using lsusb output...")
    last_present = None
    try:
        while True:
            lsusb_output = run_lsusb()
            present = keyboard_present(lsusb_output)
            if last_present is None:
                last_present = present
            if present and not last_present:
                logging.info("KEYBOARD CONNECTED (detected by lsusb)!")
                control_display_1(turn_on=False)
            elif not present and last_present:
                logging.info("KEYBOARD DISCONNECTED (detected by lsusb)!")
                control_display_1(turn_on=True)
            last_present = present
            time.sleep(interval)
    except KeyboardInterrupt:
        logging.info("Monitoring stopped by user.")

if __name__ == "__main__":
    monitor_keyboard()