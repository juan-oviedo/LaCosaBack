# chat/models/chat_models.py
from pony.orm import PrimaryKey, Required, Optional, Set
from game.models.db import db
import datetime

class ChatMessage(db.Entity):
    id = PrimaryKey(int, auto=True)
    game_id = Required(int)
    player_id = Required(int)
    player_name = Required(str)
    text = Required(str)
    timestamp = Required(datetime.datetime, default=datetime.datetime.utcnow)


# chat/models/chat_models.py
class GameLog(db.Entity):
    id = PrimaryKey(int, auto=True)
    game_id = Required(int)
    player_name = Required(str)
    action = Required(str)
    target_name = Optional(str, nullable=True)  # Cambiado a Optional
    card_data = Optional(str, nullable=True)  # Cambiado a Optional
    timestamp = Required(datetime.datetime, default=datetime.datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "game_id": self.game_id,
            "player_name": self.player_name,
            "action": self.action,
            "target_name": self.target_name,
            "card_data": self.card_data,
            "timestamp": self.timestamp,
        }