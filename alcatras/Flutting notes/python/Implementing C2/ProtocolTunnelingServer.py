# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pycryptodome"
# ]
# ///

from http.server import BaseHTTPRequestHandler, HTTPServer
from base64 import b64decode, b64encode

class C2Server(BaseHTTPRequestHandler): # это наследование в питоне типо
    def do_GET(self): # метод который вызовется когда прийдет GET запрос
        data = b64decode(self.headers["Cookie"]).decode("utf-8").rstrip()
        print(f"Recieved {data}")
        if data == "Kaori":
            response = b64encode(bytes("Recieved", "utf-8"))
            self.send_response(200)
            self.end_headers() # завершение блоков HTTP заголовков
            self.wfile.write(response)
        else:
            self.send_error(404)

if __name__ == "__main__":
    hostname = "localhost"
    port = 8443
    webServer = HTTPServer((hostname, port), C2Server)
    try:
        webServer.serve_forever() # бесконечный цикл обработки запросов
    except KeyboardInterrupt:
        pass
    webServer.server_close() # закрытие сокета