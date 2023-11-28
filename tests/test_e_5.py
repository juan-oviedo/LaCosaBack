import requests
import pytest

SERVICE_URL = "http://127.0.0.1:8000"

#test for panic cads
@pytest.mark.end2end2_test
def test_deal_card_panic(capsys):
    with capsys.disabled():
            print("\n")
            print("\tTest: deal card panic")

    cards_id = []
    for i in range(0, 137):
        cards_id.append(i)

    #create a game
    data = requests.post(f"{SERVICE_URL}/game/", json={"name": "test_game_1", "min_players": 4, "max_players": 5, "has_password": False})
    assert data.status_code == 201
    assert data.json() == {"id": 1}
    game_id = data.json()["id"]

    #create gameId
    data = requests.post(f"{SERVICE_URL}/player/join", json={"name": "test_player1", "gameId": game_id})
    assert data.status_code == 200
    assert data.json() == {"playerId": 1, "admin": True}
    player_1_id = data.json()["playerId"]

    data = requests.post(f"{SERVICE_URL}/player/join", json={"name": "test_player2", "gameId": game_id})
    assert data.status_code == 200
    assert data.json() == {"playerId": 2, "admin": False}
    player_2_id = data.json()["playerId"]

    data = requests.post(f"{SERVICE_URL}/player/join", json={"name": "test_player3", "gameId": game_id})
    assert data.status_code == 200
    assert data.json() == {"playerId": 3, "admin": False}
    player_3_id = data.json()["playerId"]

    data = requests.post(f"{SERVICE_URL}/player/join", json={"name": "test_player4", "gameId": game_id})
    assert data.status_code == 200
    assert data.json() == {"playerId": 4, "admin": False}
    player_4_id = data.json()["playerId"]

    data = requests.post(f"{SERVICE_URL}/player/join", json={"name": "test_player5", "gameId": game_id})
    assert data.status_code == 200
    assert data.json() == {"playerId": 5, "admin": False}

    #start game
    data = requests.post(f"{SERVICE_URL}/game/start", json={"id_game": game_id, "id_player": player_1_id})
    assert data.status_code == 200
    assert data.json() == {"id": game_id, "cantidad de jugadores": 5, "jugador de turno": player_1_id, "fase de turno": 1, "sentido": True}

    #check with get player status 1
    data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_1_id})
    assert data.status_code == 200
    assert data.json() == {'id': player_1_id, 'name': 'test_player1', 'position': 0, 'status': 'theThing', 'in_quarantine': False, 'quarantine_shifts': 0,
                           'cards': [{'type': 'Whisky', 'id': cards_id[133]}, 
                                    {'type': 'Infeccion', 'id': cards_id[134]}, 
                                    {'type': 'Lanzallamas', 'id': cards_id[135]}, 
                                    {'type': 'LaCosa', 'id': cards_id[136]}]}

    #check with get player status 2
    data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_2_id})
    assert data.status_code == 200
    assert data.json() == {"id": player_2_id, "name": "test_player2", "position": 1, "status": "human", 'in_quarantine': False, 'quarantine_shifts': 0,
                            'cards': [  {'type': 'CambioDeLugar', 'id': cards_id[129]},
                                        {'type': 'VigilaTusEspaldas', 'id': cards_id[130]},
                                        {'type': 'MasValeQueCorras', 'id': cards_id[131]},
                                        {'type': 'Analisis', 'id': cards_id[132]}]}
    
    #check with get player status 3
    data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_3_id})
    assert data.status_code == 200
    assert data.json() == {"id": player_3_id, "name": "test_player3", "position": 2, "status": "human", 'in_quarantine': False, 'quarantine_shifts': 0,
                            'cards': [  {'type': 'AquíEstoyBien', 'id': cards_id[125]},
                                        {'type': 'NadaDeBarbacoas', 'id': cards_id[126]},
                                        {'type': 'Seduccion', 'id': cards_id[127]},
                                        {'type': 'Sospecha', 'id': cards_id[128]}]}
    
    #check with get player status 4
    data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_4_id})
    assert data.status_code == 200
    assert data.json() == {"id": player_4_id, "name": "test_player4", "position": 3, "status": "human", 'in_quarantine': False, 'quarantine_shifts': 0,
                            'cards': [  {'type': 'Hacha', 'id': cards_id[121]},
                                        {'type': 'Aterrador', 'id': cards_id[122]},
                                        {'type': 'NoGracias', 'id': cards_id[123]},
                                        {'type': 'Fallaste', 'id': cards_id[124]}]}
    
    #check with get player status 5
    data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": 5})
    assert data.status_code == 200
    assert data.json() == {"id": 5, "name": "test_player5", "position": 4, "status": "human", 'in_quarantine': False, 'quarantine_shifts': 0,
                            'cards': [  {'type': 'Infeccion', 'id': cards_id[107]},
                                        {'type': 'Lanzallamas', 'id': cards_id[108]},
                                        {'type': 'Cuarentena', 'id': cards_id[119]},
                                        {'type': 'PuertaAtrancada', 'id': cards_id[120]}]}
    

#test for draw card panic
@pytest.mark.end2end2_test
def test_draw_card_panic(capsys):
    with capsys.disabled():
            print("\n")
            print("\tTest: draw card panic")

    cards_id = []
    for i in range(0, 137):
        cards_id.append(i + 136)

    #create a game
    data = requests.post(f"{SERVICE_URL}/game/", json={"name": "test_game_2", "min_players": 4, "max_players": 5, "has_password": False})
    assert data.status_code == 201
    assert data.json() == {"id": 2}
    game_id = data.json()["id"]

    #create gameId
    data = requests.post(f"{SERVICE_URL}/player/join", json={"name": "test_player1", "gameId": game_id})
    assert data.status_code == 200
    assert data.json() == {"playerId": 6, "admin": True}
    player_1_id = data.json()["playerId"]

    data = requests.post(f"{SERVICE_URL}/player/join", json={"name": "test_player2", "gameId": game_id})
    assert data.status_code == 200
    assert data.json() == {"playerId": 7, "admin": False}
    player_2_id = data.json()["playerId"]

    data = requests.post(f"{SERVICE_URL}/player/join", json={"name": "test_player3", "gameId": game_id})
    assert data.status_code == 200
    assert data.json() == {"playerId": 8, "admin": False}
    player_3_id = data.json()["playerId"]

    data = requests.post(f"{SERVICE_URL}/player/join", json={"name": "test_player4", "gameId": game_id})
    assert data.status_code == 200
    assert data.json() == {"playerId": 9, "admin": False}
    player_4_id = data.json()["playerId"]

    #start game
    data = requests.post(f"{SERVICE_URL}/game/start", json={"id_game": game_id, "id_player": player_1_id})
    assert data.status_code == 200
    assert data.json() == {"id": game_id, "cantidad de jugadores": 4, "jugador de turno": player_1_id, "fase de turno": 1, "sentido": True}

    #draw card player 1
    data = requests.post(f"{SERVICE_URL}/card/steal_card/{player_1_id}")
    assert data.status_code == 200
    assert data.json() ==  {'id': cards_id[120], 'type': 'PuertaAtrancada', 'number': 120, 'description': "You can't exchange cards with any player for 2 turns", "panic": False}

    #discard card player 1
    data = requests.post(f"{SERVICE_URL}/card/discard_card/{player_1_id}/{cards_id[120]}")
    assert data.status_code == 200
    assert data.json() == {'message': 'Carta desligada y marcada como descartada'}

    #change card player 1
    data = requests.post(f"{SERVICE_URL}/card/change1", json={"player_id": player_1_id, "player_to_id": player_2_id, "card_id": cards_id[134]})
    assert data.status_code == 200
    assert data.json() == {"exchange": "solicitude sent"}

    #change card player 2
    data = requests.post(f"{SERVICE_URL}/card/change2", json={"player_id": player_1_id, "player_to_id": player_2_id, "card_id2": cards_id[129]})
    assert data.status_code == 200
    assert data.json() == {"exchange": "succes"}

    #draw card player 2
    data = requests.post(f"{SERVICE_URL}/card/steal_card/{player_2_id}")
    assert data.status_code == 200
    assert data.json() == {'id': cards_id[119], 'type': 'Cuarentena', 'number': 119, 'description': 'You are in quarantine for 2 turns', "panic": False}

    #discard card player 2
    data = requests.post(f"{SERVICE_URL}/card/discard_card/{player_2_id}/{cards_id[119]}")
    assert data.status_code == 200
    assert data.json() == {'message': 'Carta desligada y marcada como descartada'}

    #change card player 2
    data = requests.post(f"{SERVICE_URL}/card/change1", json={"player_id": player_2_id, "player_to_id": player_3_id, "card_id": cards_id[132]})
    assert data.status_code == 200
    assert data.json() == {"exchange": "solicitude sent"}

    #change card player 3
    data = requests.post(f"{SERVICE_URL}/card/change2", json={"player_id": player_2_id, "player_to_id": player_3_id, "card_id2": cards_id[125]})
    assert data.status_code == 200
    assert data.json() == {"exchange": "succes"}

    #draw card player 3
    data = requests.post(f"{SERVICE_URL}/card/steal_card/{player_3_id}")
    assert data.status_code == 200
    assert data.json() == {'id': cards_id[118], 'type': 'Carta3_4', 'number': 118, 'description': 'solo para tests', "panic": True}

    #TRY play card player 3
    data = requests.post(f"{SERVICE_URL}/card/play_card1", json={"id_game": game_id, "id_player": player_3_id, "id_player_to": player_4_id, "id_card": cards_id[132]})
    assert data.status_code == 400
    assert data.json() == {"detail": "Tenes que jugar la carta de panico"}

    #TRY discard card player 3
    data = requests.post(f"{SERVICE_URL}/card/discard_card/{player_3_id}/{cards_id[132]}")
    assert data.status_code == 400
    assert data.json() == {"detail": "No se puede descartar carta en este momento"}

    #TRY discard card player 3
    data = requests.post(f"{SERVICE_URL}/card/discard_card/{player_3_id}/{cards_id[118]}")
    assert data.status_code == 400
    assert data.json() == {'detail': 'No se puede descartar carta en este momento'}

    #TRY response from player 4
    data = requests.post(f"{SERVICE_URL}/card/play_card2", json={"id_player": player_3_id, "id_player_to": player_4_id, "id_card_2": cards_id[123], "defense": True})
    assert data.status_code == 400
    assert data.json() == {'detail': 'No se puede jugar una carta de defensa en este momento'}

    #TRY change in play player 3
    data = requests.post(f"{SERVICE_URL}/card/change_in_play_1", json={"player_id": player_3_id, "player_to_id": player_4_id, "card_id": cards_id[118]})
    assert data.status_code == 400
    assert data.json() ==  {'detail': 'No se esta cambiando con el jugador correcto'}

    #TRY change in play player 4
    data = requests.post(f"{SERVICE_URL}/card/change_in_play_2", json={"player_id": player_3_id, "player_to_id": player_4_id, "card_id2": cards_id[121]})
    assert data.status_code == 400
    assert data.json() ==  {'detail': 'No se esta cambiando con el jugador correcto'}

    #play card player 3
    data = requests.post(f"{SERVICE_URL}/card/play_card1", json={"id_game": game_id, "id_player": player_3_id, "id_player_to": player_4_id, "id_card": cards_id[118]})
    assert data.status_code == 200
    assert data.json() == {'succes': True, "message": "test"}

    #change card player 3
    data = requests.post(f"{SERVICE_URL}/card/change1", json={"player_id": player_3_id, "player_to_id": player_4_id, "card_id": cards_id[128]})
    assert data.status_code == 200
    assert data.json() == {"exchange": "solicitude sent"}

    #change card player 4
    data = requests.post(f"{SERVICE_URL}/card/change2", json={"player_id": player_3_id, "player_to_id": player_4_id, "card_id2": cards_id[124]})
    assert data.status_code == 200
    assert data.json() == {"exchange": "succes"}

    #draw card player 4
    data = requests.post(f"{SERVICE_URL}/card/steal_card/{player_4_id}")
    assert data.status_code == 200
    assert data.json() == {'id': cards_id[117], 'type': 'Carta1_2', 'number': 117, 'description': 'solo para tests', "panic": True}

    #play card player 4
    data = requests.post(f"{SERVICE_URL}/card/play_card1", json={"id_game": game_id, "id_player": player_4_id, "id_player_to": player_3_id, "id_card": cards_id[117]})
    assert data.status_code == 200
    assert data.json() == {'succes': True, "message": "test"}

    #change card player 4
    data = requests.post(f"{SERVICE_URL}/card/change1", json={"player_id": player_4_id, "player_to_id": player_1_id, "card_id": cards_id[123]})
    assert data.status_code == 200
    assert data.json() == {"exchange": "solicitude sent"}

    #change card player 1
    data = requests.post(f"{SERVICE_URL}/card/change2", json={"player_id": player_4_id, "player_to_id": player_1_id, "card_id2": cards_id[135]})
    assert data.status_code == 200
    assert data.json() == {"exchange": "succes"}

    #draw card player 1
    data = requests.post(f"{SERVICE_URL}/card/steal_card/{player_1_id}")
    assert data.status_code == 200
    assert data.json() == {'id': cards_id[116], 'type': 'Olvidadizo', 'number': 116, 'description': 'solo para tests', "panic": True}

    #play card player 1
    data = requests.post(f"{SERVICE_URL}/card/play_card1", json={"id_game": game_id, "id_player": player_1_id, "id_player_to": player_4_id, "id_card": cards_id[116]})
    assert data.status_code == 200
    assert data.json() == {'succes': True, "message": "test"}

    #change card player 1
    data = requests.post(f"{SERVICE_URL}/card/change1", json={"player_id": player_1_id, "player_to_id": player_2_id, "card_id": cards_id[133]})
    assert data.status_code == 200
    assert data.json() == {"exchange": "solicitude sent"}

    #change card player 2
    data = requests.post(f"{SERVICE_URL}/card/change2", json={"player_id": player_1_id, "player_to_id": player_2_id, "card_id2": cards_id[130]})
    assert data.status_code == 200
    assert data.json() == {"exchange": "succes"}

    #draw card player 2
    data = requests.post(f"{SERVICE_URL}/card/steal_card/{player_2_id}")
    assert data.status_code == 200
    assert data.json() == {'id': cards_id[115], 'type': 'PodemosSerAmigos', 'number': 115, 'description': 'solo para tests', "panic": True}

    #play card player 2
    data = requests.post(f"{SERVICE_URL}/card/play_card1", json={"id_game": game_id, "id_player": player_2_id, "id_player_to": player_1_id, "id_card": cards_id[115]})
    assert data.status_code == 200
    assert data.json() == {'succes': True, "message": "test"}

    #change card player 2
    data = requests.post(f"{SERVICE_URL}/card/change1", json={"player_id": player_2_id, "player_to_id": player_3_id, "card_id": cards_id[131]})
    assert data.status_code == 200
    assert data.json() == {"exchange": "solicitude sent"}

    #change card player 3
    data = requests.post(f"{SERVICE_URL}/card/change2", json={"player_id": player_2_id, "player_to_id": player_3_id, "card_id2": cards_id[127]})
    assert data.status_code == 200
    assert data.json() == {"exchange": "succes"}

    #draw card player 3
    data = requests.post(f"{SERVICE_URL}/card/steal_card/{player_3_id}")
    assert data.status_code == 200
    assert data.json() == {'id': cards_id[114], 'type': 'RondaYRonda', 'number': 114, 'description': 'solo para tests', "panic": True}

    #play card player 3
    data = requests.post(f"{SERVICE_URL}/card/play_card1", json={"id_game": game_id, "id_player": player_3_id, "id_player_to": player_2_id, "id_card": cards_id[114]})
    assert data.status_code == 200
    assert data.json() == {'succes': True, "message": "test"}

    #change card player 3
    data = requests.post(f"{SERVICE_URL}/card/change1", json={"player_id": player_3_id, "player_to_id": player_4_id, "card_id": cards_id[126]})
    assert data.status_code == 200
    assert data.json() == {"exchange": "solicitude sent"}

    #change card player 4
    data = requests.post(f"{SERVICE_URL}/card/change2", json={"player_id": player_3_id, "player_to_id": player_4_id, "card_id2": cards_id[122]})
    assert data.status_code == 200
    assert data.json() == {"exchange": "succes"}

#test for Oops card panic
@pytest.mark.end2end2_test
def test_oops_card_panic(capsys):
    with capsys.disabled():
            print("\n")
            print("\tTest: oops card panic")

    cards_id = []
    for i in range(0, 137):
        cards_id.append(i + 136)
    
    game_id = 2
    player_1_id = 6
    player_2_id = 7
    player_3_id = 8
    player_4_id = 9

    #draw card player 4
    data = requests.post(f"{SERVICE_URL}/card/steal_card/{player_4_id}")
    assert data.status_code == 200
    assert data.json() ==  {'id': cards_id[113], 'type': 'Oops', 'number': 113, 'description': "Muestrales todas las cartas de tu mano a todos los jugadores", "panic": True}
    
    #play card player 4
    data = requests.post(f"{SERVICE_URL}/card/play_card1", json={"id_game": game_id, "id_player": player_4_id, "id_player_to": player_2_id, "id_card": cards_id[113]})
    assert data.status_code == 200
    assert data.json() == {'succes': True, 'message': 'Cartas del jugador mostradas'}

    #See cards player 4
    data = requests.get(f"{SERVICE_URL}/card/cards/{player_4_id}")
    assert data.status_code == 200
    assert data.json() == [{'id': 257, 'type': 'Hacha', 'number': 121, 'description': 'Kill puerta'},
                           {'id': 262, 'type': 'NadaDeBarbacoas', 'number': 126, 'description': "Sólo puedes jugar esta carta como respuesta a una carta 'Lanzallamas' para evitar ser eliminado de la partida."}, 
                           {'id': 264, 'type': 'Sospecha', 'number': 128, 'description': 'Ask for a card'},
                           {'id': 271, 'type': 'Lanzallamas', 'number': 135, 'description': 'Kill player'}]
    
    #check with get player status 4
    data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_4_id})
    assert data.status_code == 200
    assert data.json() == {'id': player_4_id, 'name': 'test_player4', 'position': 3, 'status': 'human', 'in_quarantine': False, 'quarantine_shifts': 0,
                           'cards': [{'type': 'Hacha', 'id': cards_id[121]},
                                    {'type': 'NadaDeBarbacoas', 'id': cards_id[126]},
                                    {'type': 'Sospecha', 'id': cards_id[128]},
                                    {'type': 'Lanzallamas', 'id': cards_id[135]}]}

    #change card player 4
    data = requests.post(f"{SERVICE_URL}/card/change1", json={"player_id": player_4_id, "player_to_id": player_1_id, "card_id": cards_id[135]})
    assert data.status_code == 200
    assert data.json() == {"exchange": "solicitude sent"}

    #change card player 1
    data = requests.post(f"{SERVICE_URL}/card/change2", json={"player_id": player_4_id, "player_to_id": player_1_id, "card_id2": cards_id[130]})
    assert data.status_code == 200
    assert data.json() == {"exchange": "succes"}


#test for Revelaciones card panic
@pytest.mark.end2end2_test
def test_revelaciones_card_panic(capsys):
    with capsys.disabled():
            print("\n")
            print("\tTest: revelaciones card panic")

    cards_id = []
    for i in range(0, 137):
        cards_id.append(i + 136)
    
    game_id = 2
    player_1_id = 6
    player_2_id = 7
    player_3_id = 8
    player_4_id = 9

    #draw card player 1
    data = requests.post(f"{SERVICE_URL}/card/steal_card/{player_1_id}")
    assert data.status_code == 200
    assert data.json() ==  {'id': cards_id[112], 'type': 'Revelaciones', 'number': 112, 'description':  "Empezando por ti, y siguiendo el orden del juego,cada jugador elige si revela o no su mano.La ronda de 'revelaciones' termina cuando un jugador muestre una carta, 'infeccion',sin que tenga que revelar el resto de su mano", "panic": True}
    
    #play card player 1
    data = requests.post(f"{SERVICE_URL}/card/play_card1", json={"id_game": game_id, "id_player": player_1_id, "id_player_to": player_2_id, "id_card": cards_id[112]})
    assert data.status_code == 200
    assert data.json() == {'succes': True, 'message': 'Carta de revelaciones aplicada'}

    #revelaciones player 1
    data = requests.post(f"{SERVICE_URL}/card/revelaciones", json={"id_player": player_1_id, "show_cards": True, "show_infection": False})
    assert data.status_code == 200
    assert data.json() == {'message': 'se realizo el efecto de revelaciones'}

    #See cards player 1
    data = requests.get(f"{SERVICE_URL}/card/cards/{player_1_id}")
    assert data.status_code == 200
    assert data.json() == [{'id': cards_id[123], 'type': 'NoGracias', 'number': 123, 'description': 'Sólo puedes jugar esta carta como respuesta a un ofrecimiento de intercambio de cartas.Niégate a un intercambio de cartas solicitado por un jugador o por el efecto de una carta'}, 
                           {'id': cards_id[129], 'type': 'CambioDeLugar', 'number': 129, 'description': 'Change the place physically with a player that you have next to you'}, 
                           {'id': cards_id[135], 'type': 'Lanzallamas', 'number': 135, 'description': 'Kill player'}, 
                           {'id': cards_id[136], 'type': 'LaCosa', 'number': 136, 'description': 'Tu eres LA COSA'}]
    
    #revelaciones player 2
    data = requests.post(f"{SERVICE_URL}/card/revelaciones", json={"id_player": player_2_id, "show_cards": True, "show_infection": True})
    assert data.status_code == 200
    assert data.json() ==  {'message': 'La ronda de revelaciones ya termino'}

    #See cards player 2
    data = requests.get(f"{SERVICE_URL}/card/cards/{player_2_id}")
    assert data.status_code == 404
    assert data.json() ==  {'detail': 'Carta no encontrada'}

    #TRY revelaciones player 3
    data = requests.post(f"{SERVICE_URL}/card/revelaciones", json={"id_player": player_3_id, "show_cards": True, "show_infection": False})
    assert data.status_code == 400
    assert data.json() == {'detail': 'No se puede hacer esto en este momento'}

    #See infection card player 2
    data = requests.post(f"{SERVICE_URL}/card/show_infection", params={"id_player": player_2_id})
    assert data.status_code == 200
    assert data.json() == {'id':  cards_id[134], 'type': 'Infeccion', 'number': 134, 'description': 'Esta carta te infecta, solo si la recibes luego de un intercambio de cartas'}

    #change card player 1
    data = requests.post(f"{SERVICE_URL}/card/change1", json={"player_id": player_1_id, "player_to_id": player_2_id, "card_id": cards_id[135]})
    assert data.status_code == 200
    assert data.json() == {"exchange": "solicitude sent"}

    #change card player 2
    data = requests.post(f"{SERVICE_URL}/card/change2", json={"player_id": player_1_id, "player_to_id": player_2_id, "card_id2": cards_id[127]})
    assert data.status_code == 200
    assert data.json() == {"exchange": "succes"}

#test for solo entre nosotros card panic
@pytest.mark.end2end2_test
def test_solo_entre_nosotros_card_panic(capsys):
    with capsys.disabled():
            print("\n")
            print("\tTest: solo entre nosotros card panic")

    cards_id = []
    for i in range(0, 137):
        cards_id.append(i + 136)
    
    game_id = 2
    player_1_id = 6
    player_2_id = 7
    player_3_id = 8
    player_4_id = 9

    #draw card player 2
    data = requests.post(f"{SERVICE_URL}/card/steal_card/{player_2_id}")
    assert data.status_code == 200
    assert data.json() ==  {'id': cards_id[111], 'type': 'SoloEntreNosotros', 'number': 111, 'description': "Muestra todas las cartas de tu mano a un jugador adyacente de tu eleccion", "panic": True}
    
    #play card player 2
    data = requests.post(f"{SERVICE_URL}/card/play_card1", json={"id_game": game_id, "id_player": player_2_id, "id_player_to": player_3_id, "id_card": cards_id[111]})
    assert data.status_code == 200
    assert data.json() == {'succes': True, 'message': 'Cartas mostradas'}

    #See cards player 2
    data = requests.get(f"{SERVICE_URL}/card/cards/{player_2_id}")
    assert data.status_code == 200
    assert data.json() == [{'id': cards_id[125], 'type': 'AquíEstoyBien', 'number': 125, 'description': "Sólo puedes jugar esta carta como respuesta a una carta '¡Cambio de lugar!'' o '¡Más vale que corras!''para cancelar su efecto."},
                           {'id': cards_id[133], 'type': 'Whisky', 'number': 133, 'description': 'Show all your cards to the other players. This card can only be played on yourself.'},
                           {'id': cards_id[134], 'type': 'Infeccion', 'number': 134, 'description': 'Esta carta te infecta, solo si la recibes luego de un intercambio de cartas'},
                           {'id': cards_id[135], 'type': 'Lanzallamas', 'number': 135, 'description': 'Kill player'}]

    #change card player 2
    data = requests.post(f"{SERVICE_URL}/card/change1", json={"player_id": player_2_id, "player_to_id": player_3_id, "card_id": cards_id[135]})
    assert data.status_code == 200
    assert data.json() == {"exchange": "solicitude sent"}

    #change card player 3
    data = requests.post(f"{SERVICE_URL}/card/change2", json={"player_id": player_2_id, "player_to_id": player_3_id, "card_id2": cards_id[122]})
    assert data.status_code == 200
    assert data.json() == {"exchange": "succes"}


#test for cita a ciegas card panic
@pytest.mark.end2end2_test
def test_cita_a_ciegas_card_panic(capsys):
    with capsys.disabled():
            print("\n")
            print("\tTest: cita a ciegas card panic")

    cards_id = []
    for i in range(0, 137):
        cards_id.append(i + 136)
    
    game_id = 2
    player_1_id = 6
    player_2_id = 7
    player_3_id = 8
    player_4_id = 9

    #draw card player 3
    data = requests.post(f"{SERVICE_URL}/card/steal_card/{player_3_id}")
    assert data.status_code == 200
    assert data.json() ==  {'id': cards_id[110], 'type': 'CitaACiegas', 'number': 110, 'description': "Intercambia una carta de tu mano con la primera carta del mazo,descartando cualquier carta de 'panico' robada. Tu turno termina", "panic": True}
    
    #play card player 3
    data = requests.post(f"{SERVICE_URL}/card/play_card1", json={"id_game": game_id, "id_player": player_3_id, "id_player_to": player_4_id, "id_card": cards_id[110]})
    assert data.status_code == 200
    assert data.json() == {'succes': True, 'message': 'Carta cita a ciegas aplicada'}

    #change in play player 3
    data = requests.post(f"{SERVICE_URL}/card/change_in_play_1", json={"player_id": player_3_id, "player_to_id": player_4_id, "card_id": cards_id[124]})
    assert data.status_code == 200
    assert data.json() ==  {'message': 'se intercambiaron las cartas', 'card': 'Lanzallamas'}

    #check with get player status 3
    data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_3_id})
    assert data.status_code == 200
    assert data.json() == {'id': player_3_id, 'name': 'test_player3', 'position': 2, 'status': 'human', 'in_quarantine': False, 'quarantine_shifts': 0,
                           'cards': [{'type': 'Lanzallamas', 'id': cards_id[108]},
                                      {'type': 'MasValeQueCorras', 'id': cards_id[131]},
                                      {'type': 'Analisis', 'id': cards_id[132]},
                                      {'type': 'Lanzallamas', 'id': cards_id[135]}]}

    #check with get game status
    data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": game_id})
    assert data.status_code == 200
    assert data.json() == {"gameStatus": "INIT",
                           "name": "test_game_2",
                           "players": [{"id": player_1_id, "name": "test_player1", "position": 0, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False, 'cuarentena': False},
                                       {"id": player_2_id, "name": "test_player2", "position": 1, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False, 'cuarentena': False},
                                       {"id": player_3_id, "name": "test_player3", "position": 2, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False, 'cuarentena': False},
                                       {"id": player_4_id, "name": "test_player4", "position": 3, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False, 'cuarentena': False}],
                           "gameInfo": {"sentido": "derecha",
                                       'obstaculosCuarentena': [],
                                       'obstaculosPuertaAtrancada': [],
                                       'jugadoresVivos': 4,
                                          "jugadorTurno": player_4_id,
                                          "faseDelTurno": 1,
                                          "siguienteJugador": player_1_id}}

    #draw card player 4
    data = requests.post(f"{SERVICE_URL}/card/steal_card/{player_4_id}")
    assert data.status_code == 200
    assert data.json() ==  {'id': cards_id[124], 'type': 'Fallaste', 'number': 108, 'description': "Sólo puedes jugar esta carta como respuesta a un ofrecimiento de intercambio de cartas.Niégate a un intercambio de cartas solicitado por un jugador o por el efecto de una carta.El siguiente jugador después de ti (siguiendo el orden de juego) debe intercambiar cartas en lugar de hacerlo tú.Si este jugador recibe una carta '¡Infectado!' durante el intercambio, no queda Infectado,¡pero sabrá que ha recibido una carta de La Cosa o de un jugador Infectado!Si hay 'obstáculos' en el camino, como una 'Puerta atrancada' o 'Cuarentena', no se produce ningún intercambio,y el siguiente turno lo jugará el jugador siguiente a aquel que inició el intercambio", "panic": False}
