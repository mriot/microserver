import json
import socket
import _thread


class MicroServer:
    HTTP_CODES = {
        200: "OK",
        404: "Not Found",
        500: "Internal Server Error",
    }

    def __init__(self, name="", port=8080):
        self.name = name
        self.port = port
        self.connection = None
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind(("", port))
        self._sock.listen(1)
        self._routes = {
            "/": lambda: {"name": self.name, "routes": sorted(self._routes.keys())}
        }

    def add_route(self, path, callback, nowait=False):
        if nowait:
            self._routes[path] = lambda: (_thread.start_new_thread(callback, ()), None)[1]  # type: ignore
        else:
            self._routes[path] = callback

    def _send(self, data, code=200):
        if self.connection is not None:
            content = json.dumps({"data" if code == 200 else "error": data})
            self.connection.send(
                f"HTTP/1.1 {code} {self.HTTP_CODES[code]}\r\nContent-Type: application/json\r\n\r\n{content}".encode()
            )

    def start(self):
        print(f"Server running on port {self.port}...")
        while True:
            self.connection, client_address = self._sock.accept()
            try:
                request = self.connection.recv(1024).decode().split("\r\n")
                method, route, _ = request[0].split(" ")
                print(f"{method} {route} on :{self.port} from {client_address[0]}")

                if route in self._routes:
                    self._send(self._routes[route]())
                else:
                    self._send("Route is not defined", 404)

            except Exception as e:
                print(f"Error: {e}")
                self._send(str(e), 500)

            finally:
                self.connection.close()
