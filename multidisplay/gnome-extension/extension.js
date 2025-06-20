/* exported init */

const { GLib, Gio } = imports.gi;
const Main = imports.ui.main;
const ExtensionUtils = imports.misc.extensionUtils;

const VENDOR_ID = "0b05";
const DEVICE_NAME_KEYWORDS = ["asus", "zenbook", "duo", "keyboard", "primax"];
const CHECK_INTERVAL = 2; // seconds

class AsusMultiDisplayExtension {
    constructor() {
        this._sourceId = null;
        this._lastKeyboardPresent = null;
        this._logFile = GLib.build_filenamev([GLib.get_home_dir(), '.local', 'logs', 'asus-multidisplay-extension.log']);
        
        // Ensure log directory exists
        let logDir = GLib.path_get_dirname(this._logFile);
        GLib.mkdir_with_parents(logDir, 0o755);
    }

    _log(message) {
        let timestamp = new Date().toISOString();
        let logMessage = `[${timestamp}] ${message}\n`;
        
        try {
            let file = Gio.File.new_for_path(this._logFile);
            let stream = file.append_to(Gio.FileCreateFlags.NONE, null);
            stream.write(logMessage, null);
            stream.close(null);
        } catch (e) {
            console.log(`ASUS MultiDisplay: ${message}`);
        }
    }

    _runCommand(command) {
        try {
            let [success, stdout, stderr] = GLib.spawn_command_line_sync(command);
            return {
                success: success,
                stdout: new TextDecoder().decode(stdout),
                stderr: new TextDecoder().decode(stderr)
            };
        } catch (e) {
            this._log(`Error running command "${command}": ${e.message}`);
            return { success: false, stdout: "", stderr: e.message };
        }
    }

    _isKeyboardPresent() {
        let result = this._runCommand('lsusb');
        if (!result.success) {
            return false;
        }

        let lines = result.stdout.split('\n');
        for (let line of lines) {
            let lowerLine = line.toLowerCase();
            if (lowerLine.includes(VENDOR_ID)) {
                for (let keyword of DEVICE_NAME_KEYWORDS) {
                    if (lowerLine.includes(keyword)) {
                        return true;
                    }
                }
            }
        }
        return false;
    }

    _controlDisplay(turnOn) {
        let command;
        if (turnOn) {
            command = 'gdctl set --logical-monitor --monitor eDP-1 --primary --logical-monitor --monitor eDP-2 --right-of eDP-1';
            this._log("Turning ON secondary display (keyboard disconnected)");
        } else {
            command = 'gdctl set --logical-monitor --monitor eDP-1 --primary';
            this._log("Turning OFF secondary display (keyboard connected)");
        }

        let result = this._runCommand(command);
        if (result.success) {
            this._log(`Display control successful`);
        } else {
            this._log(`Display control failed: ${result.stderr}`);
        }
    }

    _checkKeyboard() {
        let present = this._isKeyboardPresent();
        
        if (this._lastKeyboardPresent === null) {
            this._lastKeyboardPresent = present;
            this._log(`Initial keyboard state: ${present ? 'connected' : 'disconnected'}`);
            return GLib.SOURCE_CONTINUE;
        }

        if (present && !this._lastKeyboardPresent) {
            this._log("KEYBOARD CONNECTED!");
            this._controlDisplay(false); // Turn off secondary display
        } else if (!present && this._lastKeyboardPresent) {
            this._log("KEYBOARD DISCONNECTED!");
            this._controlDisplay(true); // Turn on secondary display
        }

        this._lastKeyboardPresent = present;
        return GLib.SOURCE_CONTINUE;
    }

    enable() {
        this._log("ASUS MultiDisplay Extension enabled");
        
        // Start monitoring
        this._sourceId = GLib.timeout_add_seconds(
            GLib.PRIORITY_DEFAULT,
            CHECK_INTERVAL,
            this._checkKeyboard.bind(this)
        );
        
        // Show notification
        Main.notify("ASUS MultiDisplay", "Monitoring keyboard connection status");
    }

    disable() {
        this._log("ASUS MultiDisplay Extension disabled");
        
        if (this._sourceId) {
            GLib.source_remove(this._sourceId);
            this._sourceId = null;
        }
        
        this._lastKeyboardPresent = null;
    }
}

function init() {
    return new AsusMultiDisplayExtension();
}