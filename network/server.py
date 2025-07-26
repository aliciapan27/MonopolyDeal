import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import socket
import threading

from game_logic.game import Game
from game_logic.player import Player


HOST = 'localhost'
PORT = 5555

turn_index = 0
game = None
players = []  # [(conn, name)]  eg) [(conn1, "Alicia"), (conn2, "James")]
player_objs = []
conn_map = {}
lock = threading.Lock()

def send_message(message: str, player):
    conn = conn_map.get(player.name)
    if conn:
        try:
            conn.sendall(f"{message}\n".encode())
        except:
            print(f"[ERROR] Failed to send message to {player.name}")


def handle_client(conn, addr):
    global turn_index, game

    # Ask for player name
    conn.sendall("Enter your player name: ".encode())
    name = conn.recv(1024).decode().strip()
    print(f"[CONNECTED] {name} joined from {addr}")

    player = Player(name)
    
    with lock:
        players.append((conn, name))
        player_objs.append(player)
        conn_map[name] = conn

        if len(players) == 2:
            print("[GAME READY] Two players connected.")
            game = Game(player_objs)
            game.start()

            broadcast("🎮 Game starting with two players!\n")
            broadcast(f"🟢 {players[turn_index][1]}'s turn\n")

            send_message(player.get_hand_string(), player)

    while True:
        try:
            msg = conn.recv(1024).decode().strip()
            if not msg:
                break

            if msg.lower() == "q":
                print(f"[DISCONNECTED] {name} left.")
                break

            with lock:
                current_conn, current_name = players[turn_index]

                #PLAYER
                if conn == current_conn:
                    player_obj = player_objs[turn_index]

                    broadcast(f"{name}: {msg}\n")
                    turn_index = (turn_index + 1) % 2
                    broadcast(f"🟢 {players[turn_index][1]}'s turn\n")
                else:
                    conn.sendall("⛔ Not your turn!\n".encode())
        except:
            break

    conn.close()

def broadcast(message):
    for conn, _ in players:
        try:
            conn.sendall(message.encode())
        except:
            pass

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(2)
    print(f"[SERVER] Listening on {HOST}:{PORT}")

    while len(players) < 2:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
