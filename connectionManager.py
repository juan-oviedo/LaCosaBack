import time
import asyncio
from typing import List, Dict, Tuple
from fastapi import WebSocket, WebSocketDisconnect


class ConnectionManager():
    def __init__(self):
        self.lobby_connections: List[WebSocket] = []
        self.player_connections: Dict[Tuple[int, int], WebSocket] = {}
        self.initialized: bool = False
        self.last_ws_message: Dict[Tuple[int, int], any] = {}

    async def connect_lobby(self, websocket: WebSocket):
        await websocket.accept()
        self.lobby_connections.append(websocket)

    def disconnect_lobby(self, websocket: WebSocket):
        self.lobby_connections.remove(websocket)

    async def connect_game(self, websocket: WebSocket, game_id: int):
        await websocket.accept()
        self.lobby_connections.append(websocket)

    def disconnect_game(self, websocket: WebSocket, game_id: int):
        self.lobby_connections.remove(websocket)

    async def connect_player(self, websocket: WebSocket, game_id: int, player_id: int):
        await websocket.accept()
        key = (game_id, player_id)
        if key not in self.player_connections:
            self.player_connections[key] = websocket
            print("Player connected: ", key)
            if (not self.initialized):
                self.initialized = True

    def get_last_message(self, game_id: int, player_id: int):
        key = (game_id, player_id)
        print("All last messages and keys: ", self.last_ws_message)
        if key in self.last_ws_message:
            return self.last_ws_message[key]
        else:
            return None

    def clean_last_message(self, game_id: int):
        self.last_ws_message = {
            key: value for key, value in self.last_ws_message.items() if key[0] != game_id}

    def set_last_message(self, game_id: int, player_id: int, message: any):
        # remove the last message if it exists
        self.clean_last_message(game_id)
        # set the new last message
        key = (game_id, player_id)
        self.last_ws_message[key] = message
        print("Last message set: ", key + (message,))

    def disconnect_player(self, game_id: int, player_id: int):
        key = (game_id, player_id)
        if key in self.player_connections:
            self.player_connections[key].close()
            self.player_connections.pop(key, None)
            print("Player disconnected: ", key)

    async def broadcast_json(self, message: any, dst: List[WebSocket]):
        if (not self.initialized):
            return {"type": "error", "payload": {"message": "Game not initialized"}}
        for connection in dst:
            await connection.send_json(message)

    async def send_to_player(self, game_id: int, player_id: int, message: any):
        if (not self.initialized):
            return {"type": "error", "payload": {"message": "Game not initialized"}}
        key = (game_id, player_id)
        if key in self.player_connections:
            await self.player_connections[key].send_json(message)
        else:
            print(
                f"Error in player connection. Player {player_id} not found in websocket dict: ", key)

    async def broadcast_to_game(self, game_id: int, message: any):
        if (not self.initialized):
            return {"type": "error", "payload": {"message": "Game not initialized"}}
        # Broadcast a message to all players in a game
        connections = [
            conn for key, conn in self.player_connections.items() if key[0] == game_id]
        for connection in connections:
            await connection.send_json(message)
        print(f"Broadcasted message to game {game_id}")

    async def trigger_game_status(self, game_id):
        if (not self.initialized):
            return {"type": "error", "payload": {"message": "Game not initialized"}}
        # Create the JSON message
        message = {"type": "gameStatus"}
        # Get all player connections for the specified game
        connections_to_notify = [
            ws for (g_id, _), ws in self.player_connections.items() if g_id == game_id]
        # Send the message to each player's WebSocket connection
        for connection in connections_to_notify:
            await connection.send_json(message)
        print(f"Triggered game status update for game {game_id}")

    async def trigger_player_status(self, game_id, player_id):
        if (not self.initialized):
            return {"type": "error", "payload": {"message": "Game not initialized"}}
        # Create the JSON message
        message = {"type": "playerStatus"}
        # Send the message to the player's WebSocket connection
        await self.send_to_player(game_id, player_id, message)
        print(
            f"Triggered player status update for player {player_id} in game {game_id}")

    async def send_exchange_solicitude(self, game_id, player_id, player_to_id):
        if (not self.initialized):
            return {"type": "error", "payload": {"message": "Game not initialized"}}

        # Create the JSON message, "cards" is a list of card ids that can be exchanged by player_to_id
        message = {"type": "exchangeSolicitude",
                   "payload": {"player": player_id}}
        await self.send_to_player(game_id, player_to_id, message)
        self.set_last_message(game_id, player_to_id, message)
        print(
            f"Sending exchange solicitude for player {player_to_id} in game {game_id}")

    async def send_to_player_infection(self, game_id: int, player_id: int):
        if (not self.initialized):
            return {"type": "error", "payload": {"message": "Game not initialized"}}

        message = {"type": "message", "payload": "Has sido Infectado"}
        key = (game_id, player_id)
        print("Enviando mensaje de infeccion")
        if key in self.player_connections:
            await self.player_connections[key].send_json(message)
        else:
            print(
                f"Error in player connection. Player {player_id} not found in websocket dict: ", key)

    async def send_exchange_solicitude_seduccion(self, game_id, player_id, player_to_id):
        if (not self.initialized):
            return {"type": "error", "payload": {"message": "Game not initialized"}}
        # Create the JSON message, "cards" is a list of card ids that can be exchanged by player_to_id
        message = {"type": "exchangeSolicitude_Seduccion",
                   "payload": {"player": player_id}}
        await self.send_to_player(game_id, player_to_id, message)
        self.set_last_message(game_id, player_to_id, message)
        print(
            f"Sending exchange seduccion solicitude for player {player_to_id} in game {game_id}")

    async def trigger_seduccion(self, game_id, player_id, player_to_id):
        if (not self.initialized):
            return {"type": "error", "payload": {"message": "Game not initialized"}}
        # Create the JSON message, "cards" is a list of card ids that can be exchanged by player_to_id
        message = {"type": "Seduccion", "payload": {"player_to": player_to_id}}
        await self.send_to_player(game_id, player_id, message)
        self.set_last_message(game_id, player_id, message)
        print(
            f"Sending notification of seduccion to change player {player_id} and player {player_to_id} in game {game_id}")

    async def trigger_whisky(self, game_id, player_id):
        if (not self.initialized):
            return {"type": "error", "payload": {"message": "Game not initialized"}}

        message = {"type": "Whisky", "payload": {"player": player_id}}
        await self.broadcast_to_game(game_id, message)
        print(
            f"Sending whisky message for player {player_id} in game {game_id}")

    async def trigger_play_again(self, game_id, player_id, player_to_id, card_id):
        if (not self.initialized):
            return {"type": "error", "payload": {"message": "Game not initialized"}}
        # Create the JSON message,
        message = {"type": "playAgain", "payload": {
            "player_to": player_to_id, "card_to_play": card_id}}
        await self.send_to_player(game_id, player_id, message)
        self.set_last_message(game_id, player_id, message)
        print(
            f"Sending message to play again for player {player_id} in game {game_id}")

    async def trigger_all_players_status(self, game_id):
        if (not self.initialized):
            return {"type": "error", "payload": {"message": "Game not initialized"}}
        # Create the JSON message
        message = {"type": "playerStatus"}
        # Get all player connections for the specified game
        connections_to_notify = [
            ws for (g_id, _), ws in self.player_connections.items() if g_id == game_id]
        # Send the message to each player's WebSocket connection
        for connection in connections_to_notify:
            await connection.send_json(message)
        print(f"Triggered all players status update for game {game_id}")

    async def send_defense_solicitude(self, game_id, player_id, player_to_id, def_cards):
        if (not self.initialized):
            return {"type": "error", "payload": {"message": "Game not initialized"}}

        message = {"type": "defenseSolicitude", "payload": {
            "player": player_id, "cards": def_cards}}
        await self.send_to_player(game_id, player_to_id, message)
        self.set_last_message(game_id, player_to_id, message)
        print(
            f"Sending defense solicitude for player {player_to_id} in game {game_id}")

    async def trigger_exchange_fished(self, game_id, player_id):
        if (not self.initialized):
            return {"type": "error", "payload": {"message": "Game not initialized"}}
        # Create the JSON message
        message = {"type": "exangeFished"}
        # Send the message to the player's WebSocket connection
        await self.send_to_player(game_id, player_id, message)
        self.set_last_message(game_id, player_id, message)
        print(
            f"Triggered exchange finished for player {player_id} in game {game_id}")

    async def trigger_turn_finished(self, game_id, player_id):
        if (not self.initialized):
            return {"type": "error", "payload": {"message": "Game not initialized"}}
        # Create the JSON message
        message = {"type": "turnFinished"}
        # Send the message to the player's WebSocket connection
        await self.send_to_player(game_id, player_id, message)
        self.set_last_message(game_id, player_id, message)
        print(
            f"Triggered turn finished for player {player_id} in game {game_id}")

    # creamos el trigger para visar que esta en cuarentena el jugador
    async def trigger_quarantine(self, game_id, player_id):
        if (not self.initialized):
            return {"type": "error", "payload": {"message": "Game not initialized"}}
        # Create the JSON message
        message = {"type": "quarantine", "payload": {"player": player_id}}
        # Send the message to the player's WebSocket connection
        await self.broadcast_to_game(game_id, message)
        print(f"Triggered quarantine for player {player_id} in game {game_id}")

    # creamos un trigger para avisar que se mando un mensaje a la partida
    async def trigger_chat(self, game_id):
        if (not self.initialized):
            return {"type": "error", "payload": {"message": "Game not initialized"}}
        # Create the JSON message
        message = {"type": "chat"}
        # Send the message to the player's WebSocket connection
        await self.broadcast_to_game(game_id, message)
        print(f"Triggered chat for game {game_id}")

    async def trigger_log(self, game_id):
        if (not self.initialized):
            return {"type": "error", "payload": {"message": "Game not initialized"}}
        # Create the JSON message
        message = {"type": "log"}
        # Send the message to the player's WebSocket connection
        await self.broadcast_to_game(game_id, message)
        print(f"Triggered log for game {game_id}")
    
    async def trigger_solo_entre_nosotros(self, game_id, player_id, player_to_id):
        if (not self.initialized):
            return {"type": "error", "payload": {"message": "Game not initialized"}} 
        
        message = {"type": "Whisky", "payload": {"player": player_id}}
        await self.send_to_player(game_id, player_to_id, message)
        self.set_last_message(game_id, player_to_id, message)
        print(f"Sending Solo entre nosotros message for player {player_to_id} in game {game_id}")

    async def trigger_revelaciones(self, game_id, player_id):
        if (not self.initialized):
            return {"type": "error", "payload": {"message": "Game not initialized"}} 
        
        message = {"type": "revelaciones", "payload": {"player": player_id}}
        await self.send_to_player(game_id, player_id, message)
        self.set_last_message(game_id, player_id, message)
        print(f"Sending Revelaciones message for player {player_id} in game {game_id}")

    async def show_infection(self, game_id, player_id):
        if (not self.initialized):
            return {"type": "error", "payload": {"message": "Game not initialized"}} 
        
        message = {"type": "showInfection", "payload": {"player": player_id}}
        await self.broadcast_to_game(game_id, message)
        print(f"Sending show infection message for player {player_id} in game {game_id}")

