from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import os
import numpy as np
from game.checkers import Checkers, Piece
from game.minds import MindDeepQLearning


MINIMAX_MAX_DEPTH = 4
DEEP_Q_LEARNING_MODEL_DIR = os.path.join(os.getcwd(), 'game', 'deep_q_model')

app = Flask('__name__')
CORS(app)


def make_single_move(game):
    """
    Plays a single move on the board and returns
    1 => game finished or 0 => game in progress
    """
    ai_model_name = game.ai_players[1][not game.pieces_turn]
    
    match ai_model_name:
        case 'random':
            model = {ai_model_name: ''}
        case 'minimax':
            model = {ai_model_name: MINIMAX_MAX_DEPTH}
        case 'deep_q_learning':
            model = {
                ai_model_name: MindDeepQLearning(
                input_length=len(game.board_to_tuple()) + 3,
                max_output_len=game.pieces_counter,
                model_path=DEEP_Q_LEARNING_MODEL_DIR)
                }
        case _:
            return Response('AI model not found', status=400)
        
    return game.single_move(models=model)

def validate_input(players, game=None):
    """
    Validate provided data. Check if the players are within possible options and
    empty fields are really empty
    """
    possible_player_type = (True, False)
    possible_ai_models = (None, 'random', 'minimax', 'deep_q_learning')
    
    for player_type in players[0]:
        if player_type not in possible_player_type:
            return Response('Player type was not found', status=400)
    
    for ai_model in players[1]:
        if ai_model not in possible_ai_models:
            return Response('AI model was not found', status=400)
    
    if not game:
        return 0
    
    some_counter = -1
    for ind, row in enumerate(game.board):
        for ind_r, square in enumerate(row):
            
            if ind % 2 == 0:
                some_counter *= (-1)
                
            if some_counter == 1:
                if ind_r % 2 != 0:
                    if square is not None:
                        return Response('Board discrepancy, a piece stands on a wrong square',
                                        status=400)
            else:
                if ind_r % 2 == 0:
                    if square is not None:
                        return Response('Board discrepancy, a piece stands on a wrong square',
                                        status=400)
    return 0

def convert_game_state(game_state):
    """
    Convert game state to json compatible data.
    """
    if game_state[0]:
        return (game_state[0], game_state[1], {k.id: tuple(v) for k, v in game_state[2].items()})
    else:
        return (game_state[0], game_state[1])

@app.route('/game/init', methods=['POST'])
def game_init():
    """
    Initialise a default game and send it back as a json object
    """
    
    data = request.json
    if data.get('players') is None or len(data.get('players')) != 2:
        return Response('Wrong player form', status=400)
    validate_input(players=(tuple(data['players']), (data['AIFirst'], data['AISecond'])))
    game = Checkers(
        ai_players=(tuple(data['players']), (data['AIFirst'], data['AISecond']))
    )
    
    # Make the first move if AI starts
    if game.ai_players[0][0] == True:
        game_state = make_single_move(game)
        if not game_state[0]:
            return Response('Something went wrong, a game should not have been finished after the 1st move',
                            status=400)
    else:
        game_state = game.game_over_conditions()
        
    return jsonify(**game.to_dict(), **{'game_state': convert_game_state(game_state)})

@app.route('/game/move', methods=['POST'])
def move():
    # Create a valid checkers game object from received data
    data = request.json
    data_processed = {}
    
    # Prepate the data to initialise the game
    for k, v in data.items():
        match k:
            case 'ai_players':
                data_processed[k] = tuple(map(tuple, v))
            
            case 'board':
                data_processed[k] = np.empty(shape=(data['height'], data['width']), dtype=object)
            
            case 'board_history':
                data_processed[k] = list(tuple([tuple(item[0]), item[1], item[2]]) for item in v)
            
            case 'height':
                data_processed[k] = v
            
            case 'pieces_counter':
                data_processed[k] = v
            
            case 'pieces_dark' | 'pieces_light':
                data_processed[k] = {Piece(piece[0], piece[1], tuple(piece[2]), piece[3])
                                     for piece in v}
            
            case 'pieces_turn':
                data_processed[k] = v
            
            case 'width':
                data_processed[k] = v
            
            case _:
                return Response('Sent data is not correct', status=400)
            
    for piece in (data_processed['pieces_dark'].union(data_processed['pieces_light'])):
        data_processed['board'][piece.position[0]][piece.position[1]] = piece
        
    # Initialise the object and final validation
    game = Checkers(data_processed['height'], data_processed['width'], data_processed['board'],
                    data_processed['pieces_dark'], data_processed['pieces_light'],
                    data_processed['ai_players'], data_processed['pieces_turn'],
                    data_processed['board_history'])
    validate_input(players=data_processed['ai_players'], game=game)
    
    # If its human game
    if not all(game.ai_players[0]):
        # Save the board
        game.board_history.append((game.board_to_tuple(), game.pieces_turn, game.pieces_counter))
        
        # Prepare the game for the next player
        game.pieces_turn = False if game.pieces_turn else True
    
    # Make move if it's AI turn, else check winning conditions
    if game.ai_players[0][not game.pieces_turn]:
        game_state = make_single_move(game=game)
    else:
        game_state = game.game_over_conditions()
        
    return jsonify(**game.to_dict(), **{'game_state': convert_game_state(game_state)})


if __name__ == '__main__':
    app.run(debug=True)
