from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json
import asyncio

app = FastAPI()

# Enable CORS for WebSocket connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

connections = {}  # player_id -> (websocket, player_name)

@app.websocket("/ws/{player_name}")
async def websocket_endpoint(websocket: WebSocket, player_name: str):
    await websocket.accept()
    
    player_id = id(websocket)  # simple unique id using Python's id()
    
    # Check for duplicate names
    existing_names = [name for _, name in connections.values()]
    if player_name in existing_names:
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": "Username already taken"
        }))
        await websocket.close()
        return
    
    # Save connection
    connections[player_id] = (websocket, player_name)
    
    # Debug
    print(f"Player {player_name} connected. Total players: {len(connections)}")
    print("Players connected:", [name for _, name in connections.values()])
    
    # Send welcome message to the new player
    await websocket.send_text(json.dumps({
        "type": "welcome",
        "message": f"Welcome {player_name}!"
    }))
    
    # Notify all players about the new player list
    await broadcast_player_list()
    
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received from {player_name}: {data}")
            
            # Echo message back or handle specific commands
            try:
                message = json.loads(data)
                if message.get("type") == "chat":
                    await broadcast_message(player_name, message.get("text", ""))
            except json.JSONDecodeError:
                # Handle plain text messages
                await broadcast_message(player_name, data)
                
    except WebSocketDisconnect:
        # Remove player on disconnect
        if player_id in connections:
            del connections[player_id]
            print(f"Player {player_name} disconnected. Total players: {len(connections)}")
            print("Players connected after disconnect:", [name for _, name in connections.values()])
            
            # Notify remaining players about updated player list
            await broadcast_player_list()
    except Exception as e:
        print(f"Error with {player_name}: {e}")
        if player_id in connections:
            del connections[player_id]
            await broadcast_player_list()

async def broadcast_player_list():
    """Send updated player list to all connected clients"""
    if not connections:
        return
        
    player_names = [name for _, name in connections.values()]
    message = json.dumps({
        "type": "player_list",
        "players": player_names,
        "count": len(player_names)
    })
    
    # Create a copy of connections to avoid issues with concurrent modification
    current_connections = list(connections.values())
    
    for websocket, player_name in current_connections:
        try:
            await websocket.send_text(message)
        except Exception as e:
            print(f"Failed to send to {player_name}: {e}")
            # Remove failed connection
            player_id_to_remove = None
            for pid, (ws, name) in connections.items():
                if ws == websocket:
                    player_id_to_remove = pid
                    break
            if player_id_to_remove:
                del connections[player_id_to_remove]

async def broadcast_message(sender: str, message: str):
    """Broadcast a chat message to all connected clients"""
    if not connections:
        return
        
    chat_message = json.dumps({
        "type": "chat",
        "sender": sender,
        "message": message,
        "timestamp": int(asyncio.get_event_loop().time())
    })
    
    current_connections = list(connections.values())
    
    for websocket, player_name in current_connections:
        try:
            await websocket.send_text(chat_message)
        except Exception as e:
            print(f"Failed to send chat to {player_name}: {e}")

@app.get("/")
async def root():
    return {"message": "Game Lobby WebSocket Server is running!", "players": len(connections)}

@app.get("/players")
async def get_players():
    """REST endpoint to get current players"""
    return {"players": [name for _, name in connections.values()], "count": len(connections)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)