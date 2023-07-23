from livebox.livebox import Livebox
import os
import dotenv

dotenv.load_dotenv()
livebox = Livebox(os.getenv("LIVEBOX_PASSWORD"), os.getenv("LIVEBOX_IP"))

if not livebox.wifi_enabled():
    print("Wifi is already disabled, exiting...")
    exit(0)

if livebox.is_device_connected(os.getenv("DEVICE_MAC_ADDRESS")):
    print("Cell phone is connected to the wifi, therefore user is home, exiting...")
    exit(0)

print("Cell phone is not connected to the wifi, therefore user is not home, disabling wifi...")
livebox.disable_wifi()
