import time
import json
import network
import mqtt
import neopixel
import machine

# Load configuration
with open("config.json") as f:
    config = json.load(f)

# Wi-Fi setup
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(config["wifi_ssid"], config["wifi_password"])

while not wlan.isconnected():
    time.sleep(1)

print("Connected to Wi-Fi")

# Set up MQTT
client = mqtt.MQTTClient(
    client_id=config["mqtt_client_id"],
    server=config["mqtt_broker"]
)

def on_message(topic, msg):
    print(f"Received: {topic} -> {msg}")
    # Process LED commands here

client.set_callback(on_message)
client.connect()
client.subscribe(config["mqtt_topic"])

while True:
    client.wait_msg()  # Blocking call to handle messages