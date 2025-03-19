import network
import time
import machine
import config

LED = machine.Pin(13, machine.Pin.OUT)
LED.value(1)

config.load_config()

# Connect to WiFi using config credentials
def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    ssid = config.Config['WiFi'].get('ssid', None)
    password = config.Config['WiFi'].get('password', None)
    if ssid and password:
        print("Connecting to WiFi:", ssid)
        wlan.connect(ssid, password)

        # Try for 10 seconds
        for _ in range(10):
            if wlan.isconnected():
                print("Connected! IP:", wlan.ifconfig()[0])
                return True
            time.sleep(1)
        print("Failed to connect, switching to AP mode.")
    return False

# Start up a access point
def start_ap_mode():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid="ESP32_Setup", password="12345678")
    ap.ifconfig(("192.168.4.1", "255.255.255.0", "192.168.4.1", "8.8.8.8"))
    print("Started AP Mode. Connect to 'ESP32_Setup' and visit '192.168.4.1' to configure WiFi.")

# Start AP mode if WiFi failed to connect
if not connect_to_wifi():
    start_ap_mode()