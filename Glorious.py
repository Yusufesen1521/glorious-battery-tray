# Glorious.py (English Comments)

# Required libraries
import hid
import time
import sys
import os
import logging
import queue
from queue import Queue
from threading import Thread, Event
from PIL import Image, ImageDraw, ImageFont
from pystray import MenuItem as item, Icon
from winotify import Notification

# --- SETTINGS ---
VENDOR_ID = 0x093a
PRODUCT_ID = 0x821d
TARGET_USAGE_PAGE = 65280 
QUERY_REPORT_ID = 3
QUERY_REPORT_LENGTH = 64
QUERY_PAYLOAD = bytes.fromhex(
    "03 08 fb 14 00 00 00 00 00 00 00 00 00 00 00 00 "
    "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 "
    "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 "
    "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00"
)
QUERY_INTERVAL_SECONDS = 60
RECONNECT_DELAY_SECONDS = 15
LOW_BATTERY_THRESHOLD = 20


class GloriousBatteryTrayApp:
    def __init__(self):
        self.device_path = None
        self.icon = None
        self.ui_queue = Queue()
        self.stop_event = Event()
        self._setup_logging()

    def _setup_logging(self):
        log_dir = os.path.join(os.path.expanduser("~"), "Documents", "GloriousBatteryMonitor")
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, "battery_tray_app.log")
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        logging.info("Starting System Tray Application...")

    def _create_icon_image(self, level_text: str):
        logging.info(f"Icon creation function called. Value: '{level_text}'")
        image = None
        try:
            width, height = 64, 64
            image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(image)
            try:
                font = ImageFont.truetype("arial.ttf", 40)
                logging.info("Arial font loaded successfully.")
            except IOError:
                logging.warning("Arial font not found, attempting to load default font...")
                font = ImageFont.load_default()
                logging.info("Default font loaded.")
            
            text_bbox = draw.textbbox((0, 0), level_text, font=font)
            text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
            position = ((width - text_width) / 2, (height - text_height) / 2 - 5)
            color = "white"
            try:
                level_int = int(level_text)
                if level_int <= LOW_BATTERY_THRESHOLD: color = "red"
                elif level_int > 75: color = "#66ff66" # A light green color
            except (ValueError, TypeError):
                if level_text in ["X", "!"]: color = "red"
            draw.text(position, level_text, font=font, fill=color)
            logging.info(f"Icon image successfully created for '{level_text}'.")
        except Exception as e:
            logging.error(f"!!! ICON CREATION ERROR: {e}", exc_info=True)
        return image

    def _find_device(self):
        logging.info("Searching for compatible device...")
        for dev in hid.enumerate():
            if (dev['vendor_id'] == VENDOR_ID and
                dev['product_id'] == PRODUCT_ID and
                dev['usage_page'] == TARGET_USAGE_PAGE):
                self.device_path = dev['path']
                logging.info(f"Device found: {self.device_path}")
                return True
        logging.error("Device not found.")
        return False

    def _battery_worker(self):
        device = None
        while not self.stop_event.is_set():
            try:
                if not device:
                    logging.info("Connecting to device...")
                    self.ui_queue.put(('status', '...'))
                    device = hid.device()
                    device.open_path(self.device_path)
                    logging.info("Connection successful.")
                
                device.send_feature_report(QUERY_PAYLOAD)
                time.sleep(0.05)
                resp = device.get_feature_report(QUERY_REPORT_ID, QUERY_REPORT_LENGTH)
                
                if resp and len(resp) >= 4:
                    battery_level = resp[3]
                    if 0 <= battery_level <= 100:
                        logging.info(f"Battery level read: {battery_level}%")
                        self.ui_queue.put(('level', battery_level))
                    else: 
                        logging.warning(f"Invalid battery value from device: {battery_level}")
                else: 
                    logging.warning("Received empty or invalid report from device.")
                
                self.stop_event.wait(QUERY_INTERVAL_SECONDS)

            except (OSError, IOError, ValueError) as e:
                logging.error(f"HID Error: {e}. Retrying...", exc_info=False)
                self.ui_queue.put(('status', 'X'))
                if device: 
                    device.close()
                device = None
                self.stop_event.wait(RECONNECT_DELAY_SECONDS)
        
        if device: 
            device.close()
        logging.info("Battery polling thread stopped.")
    
    def _ui_updater(self):
        logging.info("UI Updater thread started.")
        while not self.stop_event.is_set():
            try:
                msg_type, value = self.ui_queue.get(timeout=2)
                
                logging.info(f"Message received from UI queue: {msg_type}, {value}")
                
                try:
                    if msg_type == 'level':
                        level = value
                        self.icon.icon = self._create_icon_image(str(level))
                        self.icon.title = f"Glorious Battery: {level}%"
                    elif msg_type == 'status':
                        status_text = value
                        self.icon.icon = self._create_icon_image(status_text)
                        self.icon.title = f"Glorious Battery: {status_text}"
                except Exception as e:
                    logging.error(f"!!! ICON UPDATE ERROR: {e}", exc_info=True)

            except queue.Empty:
                # This is normal when there are no updates, just continue.
                pass 
            except Exception as e:
                logging.error(f"!!! UI THREAD ERROR: {e}", exc_info=True)

        logging.info("UI update thread stopped.")

    def _quit_action(self):
        logging.info("Quit action initiated...")
        self.stop_event.set()
        self.icon.stop()

    def run(self):
        if not self._find_device():
            Notification(app_id="Glorious Battery Monitor", title="Error",
                         msg="Compatible Glorious mouse not found. Please ensure it's connected.").show()
            sys.exit(1)

        menu = (item('Quit', self._quit_action),)
        try:
            initial_icon = self._create_icon_image('...')
            self.icon = Icon("GloriousBattery", initial_icon, "Glorious Battery: Starting...", menu)
            
            def setup(icon):
                # This ensures the icon is visible in the tray before starting the threads.
                icon.visible = True
                Thread(target=self._battery_worker, name="BatteryWorker", daemon=True).start()
                Thread(target=self._ui_updater, name="UIUpdater", daemon=True).start()

            self.icon.run(setup=setup)
            
        except Exception as e:
            logging.error(f"!!! APPLICATION STARTUP ERROR: {e}", exc_info=True)
            Notification(app_id="Glorious Battery Monitor", title="Critical Error",
                         msg=f"Application failed to start. Check the log file for details.\nError: {e}").show()

        logging.info("Application closed.")


if __name__ == "__main__":
    app = GloriousBatteryTrayApp()
    app.run()