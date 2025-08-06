import socket
import threading
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game_logic.game import Game
from game_logic.player import Player

HOST = '127.0.0.1'
PORT = 62743
MAX_PLAYERS = 2

class Server:
    def __init__(self):
        self.players = []
        self.conns = []
        self.shutdown_event = threading.Event()

    def handle_client(self, conn, addr):
        name = conn.recv(1024).decode().strip()
        print(f"[+] {name} joined from {addr}")
        player = Player(name, conn)
        self.players.append(player)
        self.conns.append(conn)

        if len(self.players) == MAX_PLAYERS:
            self.start_game()
    
    def start_game(self):
        print("[SERVER] Starting game...")
        game = Game(
            players=self.players,
            send_message_func=self.send_message,
            broadcast_func=self.broadcast,
            prompt_player_func=self.prompt_player,
            broadcast_others_func=self.broadcast_others,
            close_connection_func=self.close_connection
        )
        game.shutdown_event = self.shutdown_event
        game.start()

    def send_message(self, player, message):
        try:
            player.conn.sendall(message.encode() + b'\n')
        except:
            print(f"[ERROR] Couldn't send message to {player.name}")
    
    def broadcast(self, message):
        for player in self.players:
            self.send_message(player, message)
    
    def broadcast_others(self, exclude_player, message):
        for player in self.players:
            if player != exclude_player:
                self.send_message(player, message)

    def prompt_player(self, player, prompt):
        self.send_message(player, prompt)
        try:
            return player.conn.recv(1024).decode().strip()
        except:
            return 'q'

    def close_connection(self, player):
        try:
            if player.conn:
                player.conn.shutdown(socket.SHUT_RDWR)
                player.conn.close()
                print(f"[DEBUG] Closing {player.name}")
                print(f"Closed connection for player {player.name}")
        except Exception as e:
            print(f"Error closing connection for player {player.name}: {e}")

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, PORT))
            s.listen()
            s.settimeout(1.0)
            print(f"[SERVER] Listening on {HOST}:{PORT}")
            while not self.shutdown_event.is_set():
                try:
                    conn, addr = s.accept()
                    threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()

                except socket.timeout:
                    # This is expected, just loop again to check shutdown_event
                    continue
                except Exception as e:
                    print(f"[ERROR] Accept failed: {e}")
                    break
            print("[SERVER] Shutdown complete.")
            sys.exit(0) 

if __name__ == '__main__':
    Server().run()
