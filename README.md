# Microserver

A barebone python REST API server for microcontrollers running micropython.

It provides a simple way to communicate with your microcontroller over the network to let it do things like turn on a light, read a sensor, etc.

> The only dependencies are the python built-in 'json' and 'socket' modules. 

## Basics

### Create a server and give it a name

```python	
from microserver import MicroServer

server = MicroServer("Server Name")  # Default port is 8080
```
### Add routes to the server

```python
server.add_route("/hello", lambda: "Hello World!")  # => {"message": "Hello World!"}
server.add_route("/dict", lambda: {"hello": "world"})  # => {"hello": "world"}
server.add_route("/bytes", lambda: b"Hello World!")  # => {"message": "b'Hello World!'"}
```

### Start the server

Blocking

```python
server.start()
```
Or non-blocking in a new thread

```python
# micropython
import _thread
_thread.start_new_thread(server.start, ())
```

## Requests

By default the server does not actively do anything with the requests.  
It just calls the function associated with the route and returns the response.


## Responses

All responses are in JSON.

Currently `dict`, `list` and `tuple` will be directly converted to JSON before being sent.

All other types are converted to a dictionary with the key `message` and the value will be converted to a string.

### The home route `/` returns information about the server

`GET http://ADDRESS:PORT`

```json
{
    "name": "Server Name",
    "routes": [
        "/",
        "/hello"
        "/dict",

    ]
}
```

## TODO

- Custom JSON converter (for types like `bytes`, etc)
