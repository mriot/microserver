import _thread  # https://docs.micropython.org/en/latest/library/_thread.html
from microserver import MicroServer


# Create a server and give it a name
server = MicroServer("Server Name")  # Default port is 8080
server_two = MicroServer("Server Name 2", port=8081)  # NOTE: Different port

# Add routes to the server
server.add_route("/text", lambda: "Hello World!")
server.add_route("/dict", lambda: {"hello": "world"})
server.add_route("/tuple", lambda: ("Hello", "World!"))
server.add_route("/bytes", lambda: b"Hello World!")
server.add_route("/error", lambda: 1 / 0)

server_two.add_route("/text", lambda: "Hello World 2!")

# Start the server...

# ...in a new thread
_thread.start_new_thread(server_two.start, ())

# ...blocking
server.start()
