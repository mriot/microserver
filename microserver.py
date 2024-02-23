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
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ("", port)
        self.sock.bind(self.server_address)
        self.sock.listen(1)

        self.routes = {
            "/": lambda: {
                "name": self.name,
                "routes": list(self.routes.keys()),
            }
        }

    def add_route(self, path, callback):
        self.routes[path] = callback

    def _send(self, connection, data, status=200):
        content = json.dumps(
            {"data" if status == 200 else "error": data},
            default=lambda obj: str(obj),
        )
        connection.send(
            f"HTTP/1.1 {status} {self.HTTP_STATUS[status]}\r\nContent-Type: application/json\r\n\r\n{content}".encode()
        )

    def start(self):
        print(f"Server running on port {self.server_address[1]}...")
        while True:
            connection, client_address = self.sock.accept()

            try:
                data = connection.recv(1024)
                lines = data.decode().split("\r\n")
                method, route, _ = lines[0].split(" ")
                print(f"{method} {route} from {client_address[0]}")

                if route in self.routes:
                    self._send(connection, self.routes[route]())
                else:
                    self._send(connection, "Route is not defined", 404)

            except Exception as e:
                print(f"Error: {e}")
                self._send(connection, e, 500)

            finally:
                connection.close()
