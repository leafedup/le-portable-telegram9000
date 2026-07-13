import time
import urequests

URL = "http://192.168.1.x:5000/insert"  # your server address

while True:
    value = 1  # or 0
    try:
        r = urequests.post(URL, json={"value": value})
        print("Sent", value, "status", r.status_code)
        r.close()
    except Exception as e:
        print("Send failed:", e)
    time.sleep(1)