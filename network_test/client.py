import socket
import threading
import sys

shutdown_event = threading.Event()

def receive_messages(sock):
    while not shutdown_event.is_set():
        try:
            msg = sock.recv(1024)
            if not msg:
                break
            decoded = msg.decode()
            print(decoded)

            if "Server is shutting down" in decoded:
                shutdown_event.set()
                break
        except:
            break
    shutdown_event.set()

def start_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(('localhost', 5555))
    except Exception as e:
        print("Connection failed:", e)
        return

    thread = threading.Thread(target=receive_messages, args=(sock,), daemon=True)
    thread.start()

    print("Connected to server. Type messages or 'q' to quit and shut down the server.")
    try:
        while not shutdown_event.is_set():
            msg = input()
            if shutdown_event.is_set():
                break
            sock.send(msg.encode()) #sends message to server
            if msg.strip().lower() == 'q':
                break #let client exit input mode immediately, proceed to send 'q' to server to handle
    except BrokenPipeError:
        print("Server closed the connection.")
    except Exception as e:
        print("Error:", e)
    finally:
        shutdown_event.set()
        sock.close()
        print("Disconnected from server.")

if __name__ == "__main__":
    start_client()
