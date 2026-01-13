from dotenv import load_dotenv
import evdev
import requests
import os

load_dotenv()
vikunja_instance = os.getenv('vikunja_instance')
token = os.getenv('vikunja_api_token')
vikunja_headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}


devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
scanner_name = "Honeywell Scanning & Mobility  1300 Linear Imager"

for device in devices:
    if scanner_name in device.name:
        scanner_path = device.path
        break

if not scanner_path:
    print("Scanner not found.")
    exit()

scanner = evdev.InputDevice(scanner_path)
scanner.grab()

def remove_task(vikunja_task_id):
    vikunja_done_task_url = f"{vikunja_instance}/api/v1/tasks/{vikunja_task_id}"
    response = requests.post(vikunja_done_task_url, json={"done": True}, headers=vikunja_headers)


barcode = ""

for event in scanner.read_loop():
    if event.type ==evdev.ecodes.EV_KEY:
        print(evdev.categorize(event))
        data = evdev.categorize(event)
        if data.keystate == 1:
            key_code = data.keycode
            if key_code == 'KEY_LEFTSHIFT':
                continue
            if key_code == 'KEY_ENTER':
                print(barcode)
                remove_task(barcode)
                barcode = ""
            else:
                barcode += key_code.replace('KEY_', '')