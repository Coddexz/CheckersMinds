from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import os
from game.checkers import Checkers
from game.minds import MindDeepQLearning


MINIMAX_MAX_DEPTH = 4

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
            model = {ai_model_name: MindDeepQLearning(
                input_length=len(game.board_to_tuple()) + 1,
                max_output_len=game.pieces_counter,
                target_update_interval=23,
                model_path=os.path.join(os.getcwd(), 'game','deep_q_model')
                )}
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
    for ind, square in enumerate(game.board):
        if ind % 10 == 0:
            some_counter *= (-1)
            
        if some_counter == 1:
            if ind % 2 == 0:
                if square != 'None':
                    return Response('Board discrepancy, a piece stands on a wrong square',
                                    status=400)
        else:
            if ind % 2 != 0:
                if square != 'None':
                    return Response('Board discrepancy, a piece stands on a wrong square',
                                    status=400)
    return 0


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
        result = make_single_move(game)
        if result == 1:
            return Response('Something went wrong, a game should not have been finished after the 1st move',
                            status=400)
        
    return jsonify(game.to_dict())

@app.route('/game/move', methods=['POST'])
def move():
    # Makes a move on the board
    pass
    data = request.json
    

if __name__ == '__main__':
    app.run(debug=True)