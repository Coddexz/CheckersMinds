from game.checkers import Checkers
from game.minds import MindQLearning, MindDeepQLearning
import os
import time


MINIMAX_MAX_DEPTH = 4
Q_LEARNING_TRAINING_GAMES = 1000
DEEP_Q_LEARNING_TIME_LIMIT = 2
TRAIN_MORE_DEEP_Q = False


def main():
    """
    Initialise a single game.
    The game gives a brief introduction to international checkers and asks the user
    to select the type of game to be played.
    """
    print('Welcome to Checkers Minds!')
    print('Here is a brief reminder of the rules.')
    print('By default, it is an international version of checkers.')
    print('That means, that the board has 10x10 squares and 20 pieces per player.')
    print('Pieces can move diagonally one square forward or backward.')
    print('When pieces spot an enemy, they can jump over him if there is an empty square behind him.')
    print('It eliminates the opponent. If possible, the piece can make several jumps over an enemy piece.')
    print('If there is an option to jump over an enemy piece, you must do so.')
    print('You do not have to choose always the biggest number of jumps')
    print('If a piece reaches the opposite first row (e.g. 0 or 9), it becomes a king.')
    print('A king is no limited by number of squares, it can move and jump over as many squares as he wants.')
    print('As long as it is a diagonal move. A king can jump over an enemy piece in the same way as a normal piece.')
    print('The only difference is that he can choose to move to another square if it is empty.')
    print('The game is won when the other player has no more possible moves or no more pieces or kings.')
    print('It works the other way round, if you run out of moves, you lose.')
    print('The game ends in a draw if there is a King vs. King game, or if the same position is repeated')
    print('for the third time (not necessarily consecutively), with the same player having the move each time (threefold).')
    print('')
    
    print('0 --- AI vs AI (training)')
    print('1 --- AI vs AI')
    print('2 --- Human vs AI')
    print('3 --- AI vs Human')
    print('4 --- Human vs Human')
    print('Dark pieces, Light pieces\n')
    
    while True:
        try:
            game_type = int(input('Please select the type of game you wish to play (or see) by entering the correct integer.\n'))
            if game_type in range(0, 5):
                break
            else:
                print(f'Please choose a number between 0 and 4.')
        except Exception as e:
            print(e)
            print('Invalid input. Please enter a number.')
            
    training = False
    ai_model_first, ai_model_second = None, None
    if game_type == 0:
        training = True
        
    if game_type in (0, 1, 2, 3):
        ai_players = tuple()
        while True:
            print('\nChoose the AI model:')
            print('1 --- random\n2 --- minimax\n3 --- q_learning\n4 --- deep_q_learning')
            try:
                if game_type == 0 or game_type == 1 or game_type == 3:
                    ai_model_first = int(input('Choose the AI model for the first player.\n'))
                    if ai_model_first in (1, 2, 3, 4):
                        match ai_model_first:
                            case 1:
                                ai_model_first = 'random'
                            case 2:
                                ai_model_first = 'minimax'
                            case 3:
                                ai_model_first = 'q_learning'
                            case 4:
                                ai_model_first = 'deep_q_learning'
                        if game_type == 3:
                            break
                    else:
                        print('Please choose a number between 1 and 4.')
                if game_type == 0 or game_type == 1 or game_type == 2:
                    ai_model_second = int(input('Choose the AI model for the second player.\n'))
                    if ai_model_second in (1, 2, 3, 4):
                        match ai_model_second:
                            case 1:
                                ai_model_second = 'random'
                            case 2:
                                ai_model_second = 'minimax'
                            case 3:
                                ai_model_second = 'q_learning'
                            case 4:
                                ai_model_second = 'deep_q_learning'
                        break
                    else:
                        print('Please choose a number between 1 and 4.')
            except Exception as e:
                print(e)
                print('Invalid input. Please enter a number.')
        
        match game_type:
            case 0 | 1:
                ai_players = ((True, True), (ai_model_first, ai_model_second))
            case 2:
                ai_players = ((False, True), (None, ai_model_second))
            case 3:
                ai_players = ((True, False), (ai_model_first, None))
    else:
        ai_players = ((False, False), (None, None))
    
    if game_type == 4:
        models = None
    else:
        # Train AI models that need that
        models = dict()
        
        if ai_model_first =='minimax' or ai_model_second == 'minimax':
            models['minimax'] = MINIMAX_MAX_DEPTH
            
        if ai_model_first == 'q_learning' or ai_model_second == 'q_learning':
            ai_q_learning = MindQLearning()
            for n in range(Q_LEARNING_TRAINING_GAMES):
                print(f'Q_learning model playing training game {n + 1}')
                game = Checkers()
                ai_q_learning.train(game=game)
            models['q_learning'] = ai_q_learning
            
        if ai_model_first =='deep_q_learning' or ai_model_second == 'deep_q_learning':
            deep_counter = 0
            # If there is no model present
            if not os.path.isdir('deep_q_model'):
                time_start = time.time()
                ai_deep_q_learning = MindDeepQLearning(input_length=len(Checkers().board_to_tuple()) + 1,
                                                       max_output_len=Checkers().pieces_counter,
                                                       target_update_interval=23)
                while True:
                    print(f'Deep_q_learning model playing training game {deep_counter + 1}')
                    game = Checkers()
                    ai_deep_q_learning.play(game=game)
                    elapsed_time = time.time() - time_start
                    deep_counter += 1
                    if elapsed_time >= 1800 * DEEP_Q_LEARNING_TIME_LIMIT:
                        break
                ai_deep_q_learning.epsilon = -1
                ai_deep_q_learning.model_save('deep_q_model')
                models['deep_q_learning'] = ai_deep_q_learning
            else:
                ai_deep_q_learning = MindDeepQLearning(input_length=len(Checkers().board_to_tuple()) + 1,
                                                       max_output_len=Checkers().pieces_counter,
                                                       target_update_interval=23,
                                                       model_path=os.path.join(os.getcwd(), 'deep_q_model'))
                if TRAIN_MORE_DEEP_Q:
                    time_start = time.time()
                    deep_counter = 0
                    ai_deep_q_learning.epsilon = 0.6
                    while True:
                        print(f'Deep_q_learning model playing training game {deep_counter + 1}')
                        game = Checkers()
                        ai_deep_q_learning.play(game=game)
                        elapsed_time = time.time() - time_start
                        deep_counter += 1
                        if elapsed_time >= 1800 * DEEP_Q_LEARNING_TIME_LIMIT:
                            break
                    ai_deep_q_learning.epsilon = -1
                    ai_deep_q_learning.model_save('deep_q_model')
                    
                ai_deep_q_learning.epsilon = -1
                models['deep_q_learning'] = ai_deep_q_learning
    
    if training:
        while True:
            try:
                n = int(input('Please enter the number of training games you would like the AI to play.\n'))
                if n <= 0:
                    print('Please, enter a positive number')
                else:
                    break
            except Exception as e:
                print(e)
                print('Invalid input. Please enter a number.')
        train(models=models, n=n, dark_ai=ai_players[1][0], light_ai=ai_players[1][1])
        input('Press enter to exit...')
        
    else:
        game = Checkers(ai_players=ai_players)
        game.play(models=models)
        input('Press enter to exit the game...')
    
def train(models, n, dark_ai='random', light_ai='random'):
    """
    Play training games between AI.
    Prints only final score of all games.
    """
    ai_model = (dark_ai, light_ai)
    ai_players = ((True, True), ai_model)
    winners = [0, 0, 0]
    for i in range(1, n + 1):
        print(f'Playing {i} training game')
        game = Checkers(ai_players=ai_players)
        game_score = game.train(models=models)
        if game_score == 1:
            winners[0] += 1
        elif game_score == 0:
            winners[1] += 1
        else:
            winners[2] += 1
    print('finished')
    print(f'Dark: {winners[0]} --- {(winners[0] / sum(winners)) * 100:.2f}%')
    print(f'Draw: {winners[1]} --- {(winners[1] / sum(winners)) * 100:.2f}%')
    print(f'Light: {winners[2]} --- {(winners[2] / sum(winners)) * 100:.2f}%')
    

if __name__ == '__main__':
    main()