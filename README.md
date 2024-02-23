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
### Add routes

```python
server.add_route("/hello", lambda: "Hello World!")
server.add_route("/list", lambda: [1, 2, 3])
```

### Start the server

Blocking

```python
server.start()
```
Or non-blocking in a new thread

```python
import _thread
_thread.start_new_thread(server.start, ())
```

### By default the home route `/` returns information about the server

`GET http://ADDRESS:PORT/`

```json
{
    "name": "Server Name",
    "routes": [
        "/",
        "/hello"
        "/list",

    ]
}
```
> The home route can be overridden by adding a route with the path `/`.


## Requests

By default the server does not actively do anything with the requests.  
It just calls the function associated with the route and returns the response.

In most cases a simple `GET` request is enough to trigger a certain action on the microcontroller.


## Responses

All responses are in JSON.

All non-serializable types are converted to strings.

A successful response looks like this:

```json
{
    "data": "Any response data here"
}

// --- or more complex data ---

{
    "data": {
        "somekey": [
            "b'testvalue'", // bytes are converted to strings
            true
        ],
        "somedict": {
            "key": "value",
            "key2": false
        }
    }
}
```

An error response has the following format:

```json
{
    "error": "message"
}
```

### HTTP Status Codes

A small set of status codes is utilized by default:

| Code                     | Description          |
| ------------------------ | -------------------- |
| 200 &nbsp;  OK           | Successful request   |
| 404 &nbsp;  Not Found    | Route is not found   |
| 500 &nbsp;  Server Error | Something went wrong |

