import socket
import threading

clients = []
shutdown_event = threading.Event()

def handle_client(client, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    while not shutdown_event.is_set():
        try:
            msg = client.recv(1024)
            if not msg:
                break
            message = msg.decode()
            print(f"[{addr}] {message}")

            if message.strip().lower() == 'q':
                print("[SHUTDOWN] 'q' received. Shutting down.")
                shutdown_event.set()
                break

            # Relay message to all other clients
            for c in clients:
                if c != client:
                    c.send(msg)
        except:
            break
    client.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 12345))
    server.listen(2)
    server.settimeout(1)  # Check for shutdown periodically
    print("[STARTED] Server listening on port 12345")

    try:
        while not shutdown_event.is_set():
            try:
                client, addr = server.accept()
                clients.append(client)
                thread = threading.Thread(target=handle_client, args=(client, addr))
                thread.start()
            except socket.timeout:
                continue
    finally:
        print("[CLOSING] Shutting down server.")
        for c in clients:
            try:
                c.send("Server is shutting down.".encode())
                c.close()
            except:
                pass
        server.close()

if __name__ == "__main__":
    start_server()
