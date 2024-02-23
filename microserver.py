import json
import socket


class MicroServer:
    HTTP_STATUS = {
        200: "OK",
        404: "Not Found",
        500: "Internal Server Error",
    }

    def __init__(self, name, port=8080):
        self.name = name
        self.connection = None
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_address = ("", port)
        self._sock.bind(self._server_address)
        self._sock.listen(1)

        self._routes = {
            "/": lambda: {
                "name": self.name,
                "routes": list(self._routes.keys()),
            }
        }

    def add_route(self, path, callback):
        self._routes[path] = callback

    def _send(self, data, status=200):
        if self.connection is None:
            return

        content = json.dumps({"data" if status == 200 else "error": data})
        self.connection.send(
            f"HTTP/1.1 {status} {self.HTTP_STATUS[status]}\r\nContent-Type: application/json\r\n\r\n{content}".encode()
        )

    def start(self):
        print(f"Server running on port {self._server_address[1]}...")
        while True:
            self.connection, client_address = self._sock.accept()

            try:
                data = self.connection.recv(1024)
                lines = data.decode().split("\r\n")
                method, route, _ = lines[0].split(" ")

                if route in self._routes:
                    self._send(self._routes[route]())
                else:
                    self._send("Route is not defined", 404)

            except Exception as e:
                print(f"Error: {e}")
                self._send(e, 500)

            finally:
                self.connection.close()
