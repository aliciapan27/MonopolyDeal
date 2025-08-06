import socket
import threading

HOST = '127.0.0.1'
PORT = 62743

#python network/client.py
class Client:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def listen_server(self):
        while True:
            try:
                data = self.sock.recv(4096).decode()
                if data:
                    print(data.strip())
            except:
                break

    def send_loop(self):
        while True:
            try:
                msg = input()
                if msg:
                    self.sock.sendall(msg.encode())
            except:
                break

    def run(self):
        self.sock.connect((HOST, PORT))
        name = input("Enter your name: ")
        self.sock.sendall(name.encode())

        threading.Thread(target=self.listen_server, daemon=True).start()
        self.send_loop()

if __name__ == "__main__":
    Client().run()
