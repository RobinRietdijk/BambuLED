import uasyncio as asyncio
import config
import machine
import time

async def handle_request(reader, writer):
    request = await reader.read(1024)
    request = request.decode('utf-8')

    if "GET /" in request:
        # Serve Config Page
        response = f"""HTTP/1.1 200 OK\nContent-Type: text/html\n\n
        <html><body>
        <h2>ESP32 Configuration</h2>
        <form action="/config" method="post">
            <label>SSID:</label> <input name="ssid" value="{config.config_data['WiFi']['ssid']}"><br>
            <label>Password:</label> <input type="password" name="password" value="{config.config_data['WiFi']['password']}"><br>
            <button type="submit">Save & Reboot</button>
        </form>
        </body></html>"""
    
    elif "POST /config" in request:
        # Extract form data
        body = request.split("\r\n\r\n")[1]
        params = {kv.split("=")[0]: kv.split("=")[1] for kv in body.split("&")}
        
        ssid = params.get("ssid", "").replace("+", " ")
        password = params.get("password", "").replace("+", " ")

        # Update global config dictionary
        config.config_data['WiFi']['ssid'] = ssid
        config.config_data['WiFi']['password'] = password
        config.save_config()  # Save changes to file

        response = "HTTP/1.1 200 OK\nContent-Type: text/plain\n\nWiFi settings saved! Restarting..."
        
        await asyncio.sleep(2)
        machine.reset()  # Restart to apply new settings

    else:
        response = "HTTP/1.1 404 Not Found\n\n"

    writer.write(response.encode('utf-8'))
    await writer.drain()
    writer.close()
    await writer.wait_closed()

# Start the web server
async def start_server():
    server = await asyncio.start_server(handle_request, "0.0.0.0", 80)
    async with server:
        await server.serve_forever()

print("Starting Web Config Server...")
asyncio.run(start_server())

LED = machine.Pin(13, machine.Pin.OUT)
while True:
    print("Hey")
    time.sleep(3)
    LED.value(1)
    time.sleep(3)
    LED.value(0)