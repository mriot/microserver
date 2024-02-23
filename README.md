# Microserver

A minimalistic, dependency-free Python REST API server designed for microcontrollers running MicroPython.  
It offers a simple way to communicate with your microcontrollers over a network.

## Basics

### Load the code onto your microcontroller

The [microserver.py](/microserver.py) file is the only file you need to run the server.

### Create a server and optionally give it a name

```python	
from microserver import MicroServer

server = MicroServer("LED")  # Default port is 8080
```
### Add routes

```python
server.add_route("/on", lambda: led.on())
server.add_route("/off", lambda: led.off())
```

### Start the server

Blocking

```python
server.start()
```
Or non-blocking

```python
import _thread
_thread.start_new_thread(server.start, ())
```

### By default the home route `/` returns information about the server

`GET http://ADDRESS:PORT/`

```json
{
    "name": "LED",
    "routes": [
        "/",
        "/on"
        "/off",
    ]
}
```
> The home route can be overridden by adding a route with the path `/`.


## Requests

By default the server does not actively do anything with the requests.  
It just calls the function associated with the route and returns the response.

In most cases a simple `GET` request is all you need to trigger an action on the microcontroller.


## Responses

All responses are in JSON.

A successful response has the following format:

```json
{
    "data": "Any response data here"
}

// --- example ---

{
    "data": {
        "name": "LED",
        "status": "on"
    }
}
```

An error response looks like this:

```json
{
    "error": "message"
}

// --- example (404) ---

{
    "error": "Route is not defined"
}
```

In addition, a small set of http status codes is used to indicate the result of the request.

| Code                     | Description          |
| ------------------------ | -------------------- |
| 200 &nbsp;  OK           | Successful request   |
| 404 &nbsp;  Not Found    | Route is not found   |
| 500 &nbsp;  Server Error | Something went wrong |

## Multiple servers

If you, for some reason, need to run multiple servers on the same microcontroller, you can do so by creating multiple instances of `MicroServer` with different ports and starting them in separate threads.

```python
import _thread

server_two = MicroServer(port=8081)
_thread.start_new_thread(server_two.start, ())
```

## Scope of this project

This server is designed to be as simple and lightweight as possible.  
It is not intended to be a full-fledged REST API server.  

For a more feature-rich server, consider using [MicroPyServer](https://github.com/troublegum/micropyserver)

## A note on security

This server is not designed to be secure and should not be exposed to the internet.  
It is intended to be used in a local network or in a controlled environment.
