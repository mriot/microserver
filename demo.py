import _thread  # https://docs.micropython.org/en/latest/library/_thread.html
from microserver import MicroServer
from time import sleep


# Create a server and give it a name
server = MicroServer("Server Name")  # Default port is 8080

# Add routes to the server
server.add_route("/text", lambda: "Hello World!")
server.add_route("/dict", lambda: {"hello": "world"})
server.add_route("/list", lambda: ["Hello", "World!"])

# A server error
server.add_route("/error", lambda: 1 / 0)

# nowait = don't wait for the callback to finish and immediately get a response
server.add_route("/nowait", lambda: sleep(5), True)

# Create another server with a different port
server_two = MicroServer("Server Name 2", port=8081)
server_two.add_route("/text", lambda: "Hello World from the second server!")

# Start the servers...

# ...in a new thread
_thread.start_new_thread(server_two.start, ())

# ...or blocking
server.start()
