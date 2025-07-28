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

players = []  # List of (conn, name)
player_objs = []
conn_to_player = {}
shutdown_event = threading.Event()

game = None

def send_message(player, message):
    try:
        player.conn.send(message.encode())
    except Exception as e:
        print(f"[ERROR] Failed to send to client: {e}")

def broadcast(message):
    print(f"[BROADCAST] {message}")
    for player in player_objs:
        send_message(player, message)

def handle_client(conn, addr, name):
    player = conn_to_player[conn]
    print(f"[NEW CONNECTION] {name} ({addr}) connected.")
    send_message(player, f"Welcome {player.name}!")
    broadcast(f"{player.name} has joined the game.")

    while not shutdown_event.is_set():
        try:
            msg = conn.recv(1024)
            if not msg:
                break
            message = msg.decode().strip()
            print(f"[{name}] {message}")

            if message.lower() == 'q':
                print(f"[SHUTDOWN] '{name}' sent 'q'. Shutting down server.")
                broadcast("Server is shutting down.")
                shutdown_event.set()
                break
            else:
                broadcast(f"{name}: {message}")

        except:
            break

    conn.close()
    print(f"[DISCONNECT] {name} disconnected.")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(MAX_PLAYERS)
    server.settimeout(1)
    print(f"[STARTED] Server listening on {HOST}:{PORT}")

    try:
        while not shutdown_event.is_set():
            try:
                conn, addr = server.accept()
                name = f"Player{len(players) + 1}"

                # Create Player object
                player = Player(name, conn)
                player_objs.append(player)
                conn_to_player[conn] = player

                players.append((conn, name))

                thread = threading.Thread(target=handle_client, args=(conn, addr, name))
                thread.start()

                if len(players) == MAX_PLAYERS:
                    start_game()

            except socket.timeout:
                continue
    finally:
        print("[CLOSING] Shutting down server.")
        for conn, _ in players:
            try:
                conn.send("Server is shutting down.".encode())
                conn.close()
            except:
                pass
        server.close()

def start_game():
    global game
    print("[GAME] Starting the game with players:")
    for p in player_objs:
        print(f" - {p.name}")

    game = Game(player_objs, shutdown_event, send_message, broadcast)
    broadcast("All players connected.\n")
    game.start() 

if __name__ == "__main__":
    start_server()
