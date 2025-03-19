import uasyncio as asyncio
import configparser
import machine

async def handle_request(reader, writer):
    request = await reader.read(1024)
    request = request.decode('utf-8')

    if "GET /" in request:
        try:
            with open("index.html", "r") as f:
                html_content = f.read()
            response = "HTTP/1.1 200 OK\nContent-Type: text/html\n\n" + html_content
        except OSError:
            response = "HTTP/1.1 404 Not Found\n\nPage not found"

    elif "POST /config" in request:
        body = request.split("\r\n\r\n")[1]
        params = {kv.split("=")[0]: kv.split("=")[1] for kv in body.split("&")}

        ssid = params.get("ssid", "").replace("+", " ")
        password = params.get("password", "").replace("+", " ")

        configparser.Config['WiFi']['ssid'] = ssid
        configparser.Config['WiFi']['password'] = password
        configparser.save_config()

        response = "HTTP/1.1 200 OK\nContent-Type: text/plain\n\nWiFi settings saved! Restarting..."
        
        await asyncio.sleep(2)
        machine.reset()

    else:
        response = "HTTP/1.1 404 Not Found\n\n"

    writer.write(response.encode('utf-8'))
    await writer.drain()
    writer.close()
    await writer.wait_closed()

async def start():
    await asyncio.start_server(handle_request, "0.0.0.0", 80)

    while True:
        await asyncio.sleep(1)
