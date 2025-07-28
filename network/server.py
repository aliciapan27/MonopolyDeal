import sys
import os
import socket
import threading

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game_logic.game import Game
from game_logic.player import Player

HOST = 'localhost'
PORT = 5555
MAX_PLAYERS = 2

players = []              # List of (conn, name)
player_objs = []          # List of Player instances
conn_map = {}             # name -> conn
active_player = None
game = None
lock = threading.Lock()

def set_active_player(player):
    global active_player
    active_player = player

def broadcast(message):
    for conn, _ in players:
        try:
            conn.sendall(message.encode())
        except Exception as e:
            print(f"[ERROR] Failed to broadcast to a player: {e}")

def send_message(message, player):
    conn = conn_map.get(player.name)
    if conn:
        try:
            conn.sendall(message.encode())
        except Exception as e:
            print(f"[ERROR] Failed to send to {player.name}: {e}")

def prompt_player(prompt, player):
    conn = conn_map.get(player.name)
    if not conn:
        print(f"[ERROR] No connection found for {player.name}")
        return None

    try:
        conn.sendall(prompt.encode())
        response = conn.recv(1024).decode().strip()
        return response
    except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError, OSError):
        print(f"[DISCONNECTED] {player.name} disconnected during prompt.")
        global game
        if game:
            game.running = False
        broadcast(f"{player.name} disconnected. Game ended.\n")
        return None

def end_game(self, reason=""):
    
    self.broadcast("\n[DEBUG] Setting game.running to False...")
    self.running = False
    if reason:
        self.broadcast(f"\n{reason}\nGame ended.")
    else:
        self.broadcast("\nGame ended.")
    
    # Close all player connections
    for conn in conn_map.values():
        try:
            conn.sendall("DISCONNECT".encode())
            conn.close()
        except:
            pass

def handle_client(conn, addr):
    global game

    # Step 1: Get player name
    conn.sendall("Enter your player name: ".encode())
    name = conn.recv(1024).decode().strip()
    print(f"[CONNECTED] {name} joined from {addr}")
    player = Player(name)

    # Step 2: Register player safely
    with lock:
        players.append((conn, name))
        player_objs.append(player)
        conn_map[name] = conn

        if len(players) == MAX_PLAYERS:
            print("[GAME READY] Two players connected.")
            game = Game(
                player_objs,
                send_message,
                broadcast,
                prompt_player,
                set_active_player,
                end_game
            )
            threading.Thread(target=game.start, daemon=True).start()

    # Step 3: Maintain connection
    try:
        while True:
            if game is None or player != active_player:
                data = conn.recv(1024)
                if not data:
                    break
                # Ignore non-turn input, or you could add chat, etc.
            else:
                threading.Event().wait(0.1)  # Prevent busy-wait
    except:
        pass

    print(f"[DISCONNECTED] {name}")
    conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(MAX_PLAYERS)
    print(f"[SERVER] Listening on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        thread.start()

if __name__ == "__main__":
    start_server()
