- So my first template was something like this:
- I will be using telnet as my tool to connect to the server

```sh
import socket
import ipaddress

host = '127.0.0.1'
port = 8000


def main():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('127.0.0.1', 8000)) # <-- Why didnt I just use host and port instead of typing it manually...
    serversocket.listen(2)


if __name__ == '__main__':
    main() this is waht i have so far
```

**and i realized I need to add a while true loop to actually use the server even though it did cross my mind that it could be less efficient with the cpu usage i just wanted to see if it works, **

```sh
import socket

host = '127.0.0.1'
port = 8000

def main():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((host, port))
    serversocket.listen(2)
    print(f"Server is waiting on {host}:{port}")
    while True:
        connection, address = serversocket.accept()
        print(f"Connected by: {address}")
        data = connection.recv(1024)
        
        if data:
            print(f"Received: {data.decode()}")
            connection.send(data)
        connection.close()

if __name__ == '__main__':
    main()
```

**I then researched a bit and asked gpt how could i improve this further since it was lacking a little to me
he suggested i add threading to optimize it so i tried doing so and it worked but still not what i wanted**

```sh
import socket
import threading

host = '127.0.0.1'
port = 8000

def handle_client(connection, address):
    print(f"[NEW CONNECTION] {address} connected.")
    try:
        buffer = connection.recv(1024)
        if buffer:
            print(f"[{address}] says: {buffer.decode()}")
            connection.send(buffer)
    finally:
        connection.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen()
    print(f"[LISTENING] Server is starting on {host}:{port}")

    while True:
        connection, address = server.accept()
        thread = threading.Thread(target=handle_client, args=(connection, address))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == '__main__':
    main()
```

**As you can see i added threading to the server but still not what i was looking for ever though the connection was there
I asked gemini what could be improved and how I can optimize the server further and also wanted to have logs of the keys pressed on the other client until they press Ctrl C to exit out of the connection. He suggested i use asyncio which i have never heared of before so i researched and got to work and this seamed way better than before**

```sh
import asyncio

IP = '127.0.0.1'
PORT = 8000


async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"[!] {addr} joined the chat.")

    try:
        while True:
            data = await reader.read(1024)
            if not data:
                print(f"[i] {addr} left the chat (Disconnected).")
                break
            message = data.decode().strip()
            print(f"[{addr}] says: {message}")
            writer.write(f"Received: {message}\r\n".encode()) # Before adding the \r when i typed on the telnet client it would bug out 
            await writer.drain()

    except Exception as e:
        print(f"[!] Error with {addr}: {e}")
    finally:
        writer.close()
        await writer.wait_closed()


async def main():
    server = await asyncio.start_server(handle_client, IP, PORT)
    print(f"[*] Server Online at {IP}:{PORT}")
    print("[*] Monitoring all input... (Press Ctrl+C HERE to shut down server)")

    async with server:
        try:
            await server.serve_forever()
        except KeyboardInterrupt:
            print("\n[!] Server shutting down by admin.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass

```
