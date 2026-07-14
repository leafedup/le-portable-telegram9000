import network
import time

SSID = "your-ssid"
PASSWORD = "your-password"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

if not wlan.isconnected():
    wlan.connect(SSID, PASSWORD)
    for _ in range(20):
        if wlan.isconnected():
            break
        time.sleep(1)

if not wlan.isconnected():
    raise RuntimeError("WiFi connection failed")

print("Connected, IP:", wlan.ifconfig()[0])