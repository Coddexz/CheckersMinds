from checkers import Checkers


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
    if game_type == 0:
        training = True
        
    if game_type in (0, 1, 2, 3):
        ai_players = tuple()
        while True:
            print('\nChoose the AI model:')
            print('1 --- random\n2 --- minimax')
            try:
                if game_type == 0 or game_type == 1 or game_type == 3:
                    ai_model_first = int(input('Choose the AI model for the first player.\n'))
                    if ai_model_first in (1, 2):
                        ai_model_first = 'random' if ai_model_first == 1 else 'minimax'
                        if game_type == 3:
                            break
                    else:
                        print('Please choose a number between 1 and 2.')
                if game_type == 0 or game_type == 1 or game_type == 2:
                    ai_model_second = int(input('Choose the AI model for the second player.\n'))
                    if ai_model_second in (1, 2):
                        ai_model_second = 'random' if ai_model_second == 1 else 'minimax'
                        break
                    else:
                        print('Please choose a number between 1 and 2.')
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
    
    if training:
        while True:
            try:
                n = int(input('Please enter the number of training games you would like the AI to play.\n'))
                if n < 0:
                    print('Please, enter a positive number')
                else:
                    break
            except Exception as e:
                print(e)
                print('Invalid input. Please enter a number.')
        train(n=n, dark_ai=ai_players[1][0], light_ai=ai_players[1][1])
        input('Press any key to exit...')
        
    else:
        game = Checkers(ai_players=ai_players)
        game.play()
        input('Press any key to exit the game...')
    
def train(n, dark_ai='random', light_ai='random'):
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
        game_score = game.train()
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