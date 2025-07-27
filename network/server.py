import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import socket
import threading

from game_logic.game import Game
from game_logic.player import Player


HOST = 'localhost'
PORT = 5555

game = None
players = []  # [(conn, name)]  eg) [(conn1, "Alicia"), (conn2, "James")]
player_objs = []
conn_map = {}
lock = threading.Lock()

active_player = None

def set_active_player(player):
    global active_player
    active_player = player

def broadcast(message):
    for conn, _ in players:
        try:
            conn.sendall(message.encode())
        except:
            pass

def send_message(message: str, player):
    conn = conn_map.get(player.name)
    if conn:
        try:
            conn.sendall(f"{message}\n".encode())
        except:
            print(f"[ERROR] Failed to send message to {player.name}")


def prompt_player(player, prompt):
    send_message(player, prompt)
    return conn_map[player.name].recv(1024).decode().strip()

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
            game = Game(player_objs, send_message, broadcast, prompt_player, set_active_player)
            game.start()

    while True:
        try:
            msg = conn.recv(1024).decode().strip()
            if not msg:
                break

            if msg.lower() == "q":
                print(f"[DISCONNECTED] {name} left.")
                break

            with lock:
                if player != active_player:
                    conn.sendall("⛔ Not your turn!\n".encode())
                else:
                    pass
        except:
            break

    conn.close()

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
