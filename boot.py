# Pico W client: read button on GPIO2 or GPIO3 and POST 0/1 to a Python server.
# Set your Wi-Fi credentials and server address below.

import network
import socket
import time
import machine

SSID = "YOUR_WIFI_SSID"
PASSWORD = "YOUR_WIFI_PASSWORD"
SERVER_HOST = "192.168.1.100"
SERVER_PORT = 8000
SERVER_PATH = "/log"

# Use pull-down inputs. Wire buttons from GPIO2/GPIO3 to 3.3V.
pin2 = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_DOWN)
pin3 = machine.Pin(3, machine.Pin.IN, machine.Pin.PULL_DOWN)


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            time.sleep(1)
    return wlan.ifconfig()


def send_value(value):
    try:
        addr = socket.getaddrinfo(SERVER_HOST, SERVER_PORT)[0][-1]
        s = socket.socket()
        s.connect(addr)
        body = str(value)
        req = "POST {} HTTP/1.0\r\nHost: {}\r\nContent-Type: text/plain\r\nContent-Length: {}\r\n\r\n{}".format(
            SERVER_PATH, SERVER_HOST, len(body), body
        )
        s.send(req)
        s.recv(64)
    except Exception:
        pass
    finally:
        try:
            s.close()
        except Exception:
            pass


connect_wifi()
last_state = None

while True:
    if pin2.value() and not pin3.value():
        state = 0
    elif pin3.value() and not pin2.value():
        state = 1
    else:
        state = None

    if state is not None and state != last_state:
        send_value(state)
        last_state = state

    time.sleep(0.1)

# Example server (Python 3) can accept this POST and log values in SQLite.
#
# import sqlite3
# from http.server import BaseHTTPRequestHandler, HTTPServer
#
# DB = 'press_log.db'
#
# class Handler(BaseHTTPRequestHandler):
#     def do_POST(self):
#         length = int(self.headers.get('Content-Length', 0))
#         body = self.rfile.read(length).decode('utf-8')
#         if self.path == '/log' and body in ('0', '1'):
#             conn = sqlite3.connect(DB)
#             c = conn.cursor()
#             c.execute('CREATE TABLE IF NOT EXISTS events (ts TEXT, value INTEGER)')
#             c.execute('INSERT INTO events (ts, value) VALUES (datetime("now"), ?)', (int(body),))
#             conn.commit()
#             conn.close()
#             self.send_response(200)
#             self.end_headers()
#         else:
#             self.send_response(400)
#             self.end_headers()
#
# if __name__ == '__main__':
#     HTTPServer(('0.0.0.0', 8000), Handler).serve_forever()
