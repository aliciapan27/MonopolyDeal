#FastAPI WebSocket game server
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
import uuid

from game_logic.game import Game
from game_logic.player import Player

app = FastAPI()

MAX_PLAYERS = 2

connections = {}         # player_id -> websocket
players = []             # list of Player objects
game = None              # current Game instance
game_lock = asyncio.Lock()

async def send_message(player: Player, message: str):
    ws = connections.get(player.id)
    if ws:
        await ws.send_text(message)

async def broadcast(message: str):
    for ws in connections.values():
        await ws.send_text(message)

async def broadcast_others(exclude_player: Player, message: str):
    for player in players:
        if player != exclude_player:
            ws = connections.get(player.id)
            if ws:
                await ws.send_text(message)

async def prompt_player(player: Player, prompt: str) -> str:
    ws = connections.get(player.id)
    if ws:
        await ws.send_text(prompt)
        try:
            data = await ws.receive_text()
            return data.strip()
        except WebSocketDisconnect:
            return 'q'
    return 'q'

def close_connection(player: Player):
    ws = connections.pop(player.id, None)
    if ws:
        # No explicit close here, websocket disconnect handled elsewhere
        pass

@app.websocket("/ws/{player_name}")
async def websocket_endpoint(websocket: WebSocket, player_name: str):
    await websocket.accept()

    player_id = str(uuid.uuid4())
    player = Player(player_name, player_id)
    players.append(player)
    connections[player_id] = websocket

    await broadcast(f"{player_name} joined the game. Waiting for players... ({len(players)}/{MAX_PLAYERS})")

    # When enough players have joined, start the game
    if len(players) == MAX_PLAYERS:
        global game
        async with game_lock:
            if not game:
                game = Game(
                    players=players.copy(),
                    send_message_func=send_message,
                    broadcast_func=broadcast,
                    prompt_player_func=prompt_player,
                    broadcast_others_func=broadcast_others,
                    close_connection_func=close_connection
                )
                asyncio.create_task(game.start())  # assuming start() is async or runs game loop async

    try:
        while True:
            data = await websocket.receive_text()
            # Here you could process incoming messages, e.g. player commands, etc.
            # For now, just echo or ignore
            await websocket.send_text(f"Received: {data}")

    except WebSocketDisconnect:
        players.remove(player)
        connections.pop(player_id, None)
        await broadcast(f"{player_name} disconnected.")

