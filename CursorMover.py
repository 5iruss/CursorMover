import pyautogui
import random
import time
import psutil
import logging

pyautogui.FAILSAFE = False

logging.basicConfig(filename='cursor_mover.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def cursor_mover():
    screen_width, screen_height = pyautogui.size()
    start_time = time.time()

    logging.info("Cursor Mover started.")

    while time.time() - start_time < 300:
        x = random.randint(100, screen_width - 100) 
        y = random.randint(100, screen_height - 100)
        pyautogui.moveTo(x, y, duration=0.1)

        if random.random() < 0.5:
            pyautogui.click()
            logging.info(f"Clicked at ({x}, {y})")
        if random.random() < 0.3:
            pyautogui.click(button='right')
            logging.info(f"Right-clicked at ({x}, {y})")
        if random.random() < 0.2:
            pyautogui.hotkey('alt', 'tab')
            logging.info("Pressed Alt + Tab")

        time.sleep(0.5)

def check_usb_connected(previous_drives):
    current_drives = {d.device for d in psutil.disk_partitions(all=False)}
    new_drives = current_drives - previous_drives

    if new_drives:
        logging.info("USB connected! Starting Cursor Mover...")
        cursor_mover()
        return current_drives
    return previous_drives

if __name__ == "__main__":
    previous_drives = {d.device for d in psutil.disk_partitions(all=False)}
    
    logging.info("Monitoring for USB connections...")
    
    try:
        last_log_time = time.time()
        while True:
            previous_drives = check_usb_connected(previous_drives)
            current_time = time.time()
            
            if current_time - last_log_time >= 5:
                logging.info("Waiting for USB connection...")
                last_log_time = current_time
            
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Exiting...")
        print("Exiting...")
