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
