from fastapi import APIRouter, HTTPException
from pony.orm import db_session, commit, select
from .models import GameLog
from .schemas import GameLogCreate
from utils import manager
from .schemas import ChatMessageCreate, ChatMessageResponse
from .models import ChatMessage
from typing import Optional
import datetime
from game.player.models import Player



@db_session
def save_chat_message(chat_message: ChatMessageCreate):
    # Obtener el nombre del jugador a partir del player_id
    player_name = select(p.name for p in Player if p.id == chat_message.player_id).first()

    new_message = ChatMessage(
        game_id=chat_message.game_id,
        player_id=chat_message.player_id,
        text=chat_message.text,
        timestamp=datetime.datetime.utcnow(),
        player_name=player_name  # Agregar el nombre del jugador al nuevo mensaje
    )
    commit()  # Guardar el nuevo mensaje en la base de datos
    return new_message



def log_game_action(game_id: int, player_name: str, action: str, target_name: str = None, card_data: str = None):
    with db_session:
        log_data = GameLogCreate(
            game_id=game_id,
            player_name=player_name,
            action=action,
            target_name=target_name,
            card_data=card_data
        )
        new_log = GameLog(**log_data.dict())
        if target_name is not None:
            new_log.target_name = target_name  # Asignar target_name solo si no es None