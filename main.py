import uasyncio as asyncio
import machine
import time
import webserver

asyncio.create_task(webserver.start())

LED = machine.Pin(13, machine.Pin.OUT)
while True:
    time.sleep(1)