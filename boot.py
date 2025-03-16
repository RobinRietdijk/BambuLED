import machine
import network

# Set up Wi-Fi (if needed)
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Print boot message
print("Boot sequence complete.")