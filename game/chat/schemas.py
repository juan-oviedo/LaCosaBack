# chat/schemas.py
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class ChatMessageCreate(BaseModel):
    game_id: int
    player_id: int
    text: str

class ChatMessageResponse(BaseModel):
    id: int
    game_id: int
    player_id: int
    player_name: str
    text: str
    timestamp: datetime

class ChatMessageUpdate(BaseModel):
    text: Optional[str]


class GameLogCreate(BaseModel):
    game_id: int
    player_name: str
    action: str
    target_name: Optional[str] = None
    card_data: Optional[str] = None