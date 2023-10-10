from .minds import MindMinimax
import numpy as np
import random
from time import time, sleep
import os, platform


class Checkers:
    """
    Representation of the game
    """
    
    def __init__(self, height=10, width=10, board=None, pieces_dark=20, pieces_light=20,
                 ai_players=((False, True),(None, 'random')), pieces_turn=True, board_history=None):
        self.height = height
        self.width = width
        self.ai_players = ai_players
        self.pieces_turn = pieces_turn
        
        # If the board exists, then pieces_dark and light are sets of objects
        # Else, they can be int to store information about amount (custom) of pieces to create
        # If the board does not exist yet
        # if not board and not pieces_dark and not pieces_light:
        if board is None:
            self.board = np.empty(shape=(self.height, self.width), dtype=object)
            
            # Create pieces for the board, black <=> color=True
            self.pieces_dark = {Piece(id=i, color=True) for i in range(int(pieces_dark))}
            self.pieces_light = {Piece(id=i, color=False) for i in range(
                int(pieces_dark),int(pieces_light) + int(pieces_dark))}
            self.pieces_counter = len(self.pieces_dark) + len(self.pieces_light)
            self.board_history = []
            
            # Checkers spacing
            self.board_init()
            
        else:
            self.board = board
            self.pieces_dark = pieces_dark
            self.pieces_light = pieces_light
            self.pieces_counter = len(pieces_dark) + len(pieces_light)
            self.board_history = board_history
        
    # Fill the board
    def board_init(self):
        piece_id_counter = 0
        dark_pieces_c = len(self.pieces_dark)
        
        # Empty rows => 2 rows starting from the next row after the last dark piece
        # If there are too many pieces for the board => omit empty rows
        if np.floor((self.board.size - 20) / self.pieces_counter) >= 2:
            empty_row = int(np.ceil(dark_pieces_c / (self.width // 2)))
            empty_rows = [empty_row, empty_row + 1]
        else:
            empty_rows = None
            
        # Iterate over rows in the board
        for index_r in range(len(self.board)): 
            
            # Ommit 2 empty rows
            if empty_rows:
                if index_r in empty_rows:
                    continue
            
            # Depending on number, the row has first dark square or light square
            if index_r % 2 != 0:
                # Iterate over squares in the board
                for index_sq in range(len(self.board[index_r])): 
                    # If the square is black
                    if index_sq % 2 == 0:
                        
                        # Initialize piece to None before the loops
                        piece = None
                        
                        # Create a piece (light or black) and store it in the dict
                        # dark <=> color=True and first 20 pieces
                        if piece_id_counter < dark_pieces_c:
                            
                            # Set the right piece on the board
                            for i in self.pieces_dark: 
                                if i.id == piece_id_counter:
                                    piece = i
                                    break
                        else:
                            # Change the row if the row is occupied with any black piece already
                            if any(i.color == True for i in self.board[index_r] if i != None):
                                continue
                            # Set the right piece on the board
                            for i in self.pieces_light: 
                                if i.id == piece_id_counter:
                                    piece = i
                                    break
                        
                        # In case piece was not found
                        if piece is None:
                            # If all pieces are set => finish the method, else raise error
                            if piece_id_counter == self.pieces_counter:
                                return 0
                            raise Exception('Piece was not found')
                        
                        # Store the piece on the board
                        self.board[index_r][index_sq] = piece 
                        piece.position = (index_r, index_sq)
                        piece_id_counter += 1
                    else:
                        continue
            
            else:
                # Iterate over squares in the board
                for index_sq in range(len(self.board[index_r])): 
                    # If the square is black
                    if index_sq % 2 != 0:
                        
                        # Initialize piece to None before the loops
                        piece = None
                        # Create a piece (light or black) and store it in the dict
                        # dark <=> color=True and first 20 pieces
                        if piece_id_counter < dark_pieces_c:
                            
                            # Set the right piece on the board
                            for i in self.pieces_dark: 
                                if i.id == piece_id_counter:
                                    piece = i
                                    break
                        else:
                            # Change the row if the row is occupied with any black piece already
                            if any(i.color == True for i in self.board[index_r] if i != None):
                                continue
                            # Set the right piece on the board
                            for i in self.pieces_light: 
                                if i.id == piece_id_counter:
                                    piece = i
                                    break
                        
                        # In case piece was not found
                        if piece is None:
                            # If all pieces are set => finish the method, else raise error
                            if piece_id_counter == self.pieces_counter:
                                return 0
                            raise Exception('Piece was not found')
                        
                        # Store the piece on the board
                        self.board[index_r][index_sq] = piece 
                        piece.position = (index_r, index_sq)
                        piece_id_counter += 1
                    else:
                        continue
        
        # If not all pieces have been spaced return failure
        if self.pieces_counter != piece_id_counter:
            return 1
        # The method has been successfully finished
        return 0
 
    def set_possible_moves(self):
        """
        Return a dict with every possible move for the current player
        Store moves according to this schema:
        {piece: {((move), value)}}
        value = False if the field is empty else value = True
        Jumping over has precedence over moving to an empty field
        multiple moves => {piece: {(((move_1), move_2), value)}}
        """    
        
        # Get the right player
        player = self.pieces_turn
        # Function checking for multiple jumps
        def check_multiple_jumps(piece, piece_pos, piece_king, defeated_pieces,
                                 piece_multi_jumps, jump_series=None):
            # At the beginning append the possible jump to the series
            if jump_series == None:
                jump_series = []
            jump_series.append((piece_pos[0], piece_pos[1]))
            jump_counter = 0
            
            if not piece_king:
                # Iterate over every possible next movement
                for n_row in [-1, 1]:
                    for n_col in [-abs(n_row), abs(n_row)]:
                        allowed_row, allowed_col = piece_pos[0] + n_row, piece_pos[1] + n_col
                        
                        # If not within board bounadaries
                        if not (0 <= allowed_row < self.height and 0 <= allowed_col < self.width):
                            continue
                        
                        # Only different enemy piece is a valid possibility to move
                        next_square = self.board[allowed_row][allowed_col]
                        # If next_square is the current piece => treat it as an empty square
                        if next_square == piece:
                            next_square = None
                            
                        if isinstance(next_square, Piece) and next_square.color != player and \
                            next_square not in defeated_pieces:
                            # Check if the square behind enemy is empty
                            bh_n_row, bh_n_col = allowed_row + n_row, allowed_col + n_col
                            
                            # If not within board bounadaries
                            if not (0 <= bh_n_row < self.height and 0 <= bh_n_col < self.width):
                                continue
                            # If the square behind is an empty square or the current piece =>
                            # => start the function again
                            # Add enemy piece to defeated list, to not to fall into infinite an loop
                            elif self.board[bh_n_row][bh_n_col] is None or \
                                self.board[bh_n_row][bh_n_col] == piece:
                                jump_counter += 1
                                defeated_pieces.add(next_square)
                                
                                # Every jump keeps information about the list containing all the series,
                                # every time create a new jump_series and defeated_pieces series and
                                # pass them, to keep series specific data 
                                check_multiple_jumps(
                                    piece=piece,
                                    piece_pos=(bh_n_row, bh_n_col),
                                    piece_king=False,
                                    piece_multi_jumps=piece_multi_jumps,
                                    jump_series=[i for i in jump_series],
                                    defeated_pieces={i for i in defeated_pieces})

                # If there was no possible jump => store the series in main list with all jumps
                if jump_counter == 0:
                    piece_multi_jumps.append(jump_series)
                
                return piece_multi_jumps
                                
            # If a king
            else:
                # Iterate over every possible next movement
                for n_row in [i for i in range(-self.height + 1, self.height) if i != 0]:
                    for n_col in [-abs(n_row), abs(n_row)]:
                        allowed_row, allowed_col = piece_pos[0] + n_row, piece_pos[1] + n_col
                        eq_al_row = 1 if n_row > 0 else -1
                        eq_al_col = 1 if n_col > 0 else -1
                        
                        # If not within board bounadaries
                        if not (0 <= allowed_row < self.height and 0 <= allowed_col < self.width):
                            continue
                        
                        # Only different enemy piece is a valid possibility to move
                        next_square = self.board[allowed_row][allowed_col]
                        # if piece_king and piece_pos[0] == 4 and piece_pos[1] == 3 and len(jump_series) == 4 and (allowed_row == 5 or allowed_row == 2):
                        #     print('Yeah')
                        # If next_square is the current piece => treat it as an empty square
                        if next_square == piece:
                            next_square = None
                            
                        if isinstance(next_square, Piece) and next_square.color != player and \
                            next_square not in defeated_pieces:
                                
                            # Check whether the previous squares are empty if the square is not adjacent
                            if abs(piece_pos[0] - allowed_row) > 1:
                                # Create presumption of correctness
                                correct = True
                                temp_mov_r = (piece_pos[0], piece_pos[1])
                                # As long as it is a valid move, equalise position
                                while abs(allowed_row - temp_mov_r[0]) > 1:
                                    temp_mov_r = (temp_mov_r[0] + eq_al_row, temp_mov_r[1] + eq_al_col)
                                    # To jump over the other player's piece, squares before have to be empty
                                    if self.board[temp_mov_r[0]][temp_mov_r[1]] is not None and \
                                        self.board[temp_mov_r[0]][temp_mov_r[1]] is not piece:
                                        correct = False
                                        break
                                    
                                # If not correct king move
                                if not correct:
                                    continue
                                    
                            # Check if the square behing enemy is empty
                            bh_n_row, bh_n_col = allowed_row + eq_al_row, allowed_col + eq_al_col
                            
                            # Add every possible move (single jump)
                            while 0 <= bh_n_row < self.height and 0 <= bh_n_col < self.width and \
                                (self.board[bh_n_row][bh_n_col] is None or
                                 self.board[bh_n_row][bh_n_col] is piece):
                                    jump_counter += 1
                                    defeated_pieces.add(next_square)
                            # Every jump keeps information about the list containing all the series,
                            # every time create a new jump_series and defeated_pieces series and
                            # pass them, to keep series specific data 
                                    check_multiple_jumps(
                                        piece=piece,
                                        piece_pos=(bh_n_row, bh_n_col),
                                        piece_king=True,
                                        piece_multi_jumps=piece_multi_jumps,
                                        jump_series=[i for i in jump_series],
                                        defeated_pieces={i for i in defeated_pieces})
                                    # Check next square
                                    bh_n_row += eq_al_row
                                    bh_n_col += eq_al_col
                                    

                # If there was no possible jump => store the series in main list with all jumps
                if jump_counter == 0:
                    piece_multi_jumps.append(jump_series)
                
                return piece_multi_jumps
        
        # Get the right set of pieces
        pieces = self.pieces_dark if player else self.pieces_light
        possible_moves = dict()
        
        # Iterate over every piece and check for possible moves
        for piece in pieces:
            # Get the position
            row, col = piece.position[0], piece.position[1]
            
            # Check possible moves for uncrowned pieces
            if not piece.king:
                
                # Temporary store possible moves of a piece
                piece_free_moves = set()
            
                # Get and check every selected square for an important move
                # For every row check, for the same +- number of columns to move diagonally
                for d_row in [-1, 1]:
                    for d_col in [-abs(d_row), abs(d_row)]:
                        sel_row = row + d_row
                        sel_col = col + d_col
                        
                        # Check if the selected position is within the board boundaries
                        if 0 <= sel_row < self.height and 0 <= sel_col < self.width:
                            selected_square = self.board[sel_row][sel_col]
                            
                            # Check whether the square is empty, occupied by enemy or meaningless
                            if selected_square is None:
                                piece_free_moves.add(((sel_row, sel_col), False))
                                
                            elif isinstance(selected_square, Piece) and selected_square.color != player:
                                
                                # Check if the square behind the enemy is empty
                                bh_enemy_sel_row, bh_enemy_sel_col = sel_row + d_row, sel_col + d_col
                                
                                # Check if the square is within the board boundaries
                                if 0 <= bh_enemy_sel_row < self.height and 0 <= bh_enemy_sel_col < self.width and \
                                    self.board[bh_enemy_sel_row][bh_enemy_sel_col] is None:
                                        
                                    # Check for multiple jumps
                                    # Create a list to store all possible jumps (finished =>
                                    # => not possible to jump anymore)
                                    # Start the recursion with crucial information like position, is king and
                                    # defeated piece
                                    
                                    all_beating_jumps = check_multiple_jumps(piece=piece,
                                                        piece_pos=(bh_enemy_sel_row, bh_enemy_sel_col),
                                                         defeated_pieces={selected_square},
                                                         piece_multi_jumps=[], piece_king=False)
                                    # Add every move according to the schema
                                    for jump in all_beating_jumps:
                                        piece_free_moves.add((tuple(jump), True))
                        
            # Check moves for kings
            else:
            
                # Temporary store possible moves of a piece
                piece_free_moves = set()
                
                # Get and check every selected square for an important move
                # For every row check, for the same +- number of columns to move diagonally
                for d_row in [i for i in range(-self.height + 1, self.height) if i != 0]:
                    for d_col in [-abs(d_row), abs(d_row)]:
                        sel_row = row + d_row
                        sel_col = col + d_col
                        # Choose the sign for equalising
                        row_eq = 1 if d_row > 0 else -1
                        col_eq = 1 if d_col > 0 else -1
                    
                        # Check if the selected position is within the board boundaries
                        # and the position is not already added
                        if 0 <= sel_row < self.height and 0 <= sel_col < self.width and \
                            not any(move_jump[0] == (sel_row, sel_col) for move_jump in piece_free_moves):
                            selected_square = self.board[sel_row][sel_col]
                        
                            # Check whether the square is empty, occupied by enemy or meaningless
                            if selected_square is None:
                                
                                # If this is a long move, check every empty square
                                # Initialise empty set for optimisation
                                right_moves = set()
                                temp_mov = (row, col)
                                # As long as it is a move and has not been added, equalise positions
                                while abs(sel_row - temp_mov[0]) >= 1:
                                    temp_mov = (temp_mov[0] + row_eq, temp_mov[1] + col_eq)
                                    # Add moves to empty squares only
                                    if self.board[temp_mov[0]][temp_mov[1]] is None:
                                        # Add only if wasn't added earlier
                                        if (temp_mov, False) not in piece_free_moves:
                                            right_moves.add(temp_mov)
                                        else:
                                            continue
                                    else:
                                        break
                                        
                                # Add possible empty square moves,
                                # every move is right as the loop start from the piece's position
                                for move in right_moves:
                                    piece_free_moves.add((move, False))
                            
                            # If a piece meets a piece of the other player
                            elif isinstance(selected_square, Piece) and selected_square.color != player:
                                
                                # Check whether the previous squares are empty if the square is not adjacent
                                if abs(row - sel_row) > 1:
                                    # Initialise empty set for optimisation and create presumption of correctness
                                    right_moves = set()
                                    correct = True
                                    temp_mov = (row, col)
                                    # As long as it is a move and has not been spotted before, equalise position
                                    while abs(sel_row - temp_mov[0]) > 1:
                                        temp_mov = (temp_mov[0] + row_eq, temp_mov[1] + col_eq)
                                        # To jump over the other player's piece, squares before have to be empty
                                        # Do not consider already know empty squares
                                        if (temp_mov, False) in piece_free_moves:
                                            continue
                                        elif self.board[temp_mov[0]][temp_mov[1]] is not None:
                                            correct = False
                                            break
                                        right_moves.add(temp_mov)
                                        
                                    # Add possible empty square moves,
                                    # every move is right as the loop start from the piece's position,
                                    # value=False, because it checks squares before the enemy piece
                                    for move in right_moves:
                                        piece_free_moves.add((move, False))
                                        
                                    # If not correct king move
                                    if not correct:
                                        continue
                                
                                # Check if the square behind the enemy is empty
                                bh_enemy_sel_row, bh_enemy_sel_col = sel_row + row_eq, sel_col + col_eq
                                    
                                # Add every possible move (single jump)
                                while 0 <= bh_enemy_sel_row < self.height and 0 <= bh_enemy_sel_col < self.width and \
                                    self.board[bh_enemy_sel_row][bh_enemy_sel_col] is None:
                                    # Check for multiple jumps
                                    # Create a list to store all possible jumps (finished =>
                                    # => not possible to jump anymore)
                                    # Start the recursion with crucial information like position, is king and
                                    # defeated piece
                                    
                                    all_beating_jumps = check_multiple_jumps(piece=piece,
                                                         piece_pos=(bh_enemy_sel_row, bh_enemy_sel_col),
                                                         defeated_pieces={selected_square},
                                                         piece_multi_jumps=[], piece_king=True)
                                    # Add every move according to the schema
                                    for jump in all_beating_jumps:
                                        piece_free_moves.add((tuple(jump), True))
                                    # piece_free_moves.add(((bh_enemy_sel_row, bh_enemy_sel_col), True))
                                    # Check next square
                                    bh_enemy_sel_row += row_eq
                                    bh_enemy_sel_col += col_eq

                            # else:
                            #     # print('Invalid move')
                            #     continue
                            
            # Store moves
            if piece_free_moves:
                possible_moves[piece] = piece_free_moves 
            
        # Return only key moves, i.e. value=True or value=False for every move
        # First, check if there are any jumping moves, then return a correct dict, i. e.
        # only with or without jumping over enemy piece
        jumping = any(move[1] for moves in possible_moves.values() for move in moves)
        if jumping:
            return {piece: {move for move in moves if move[1]}
                    for piece, moves in possible_moves.items()
                    if any(move[1] for move in moves)}
        return possible_moves
    
    # Let's play a game
    def play(self, models):
        
        # Check the state of the game
        computer_system = platform.system()
        game_state = tuple(self.game_over_conditions())
        if not game_state[0]:
            return game_state[1]
        
        # Check how many AI is in the game
        # AI plays against itself
        if all(self.ai_players[0]):
            # Get the ai settings
            dark_ai = (self.ai_players[0][0], self.ai_players[1][0])
            light_ai = (self.ai_players[0][1], self.ai_players[1][1])
            
            while game_state[0]:
                
                self.board_print()
                print('')
                ai_settings = ('Dark', dark_ai[1]) if self.pieces_turn else ('Light', light_ai[1])
                print(f'{ai_settings[0]} AI is making a move ...')
                
                match ai_settings[1]:
                    
                    # AI makes always random moves
                    case 'random':
                        sleep(3)
                        random_piece = random.choice(list(game_state[2].keys()))
                        random_move_value = random.choice(list(i for i in game_state[2][random_piece]))
                        action, jump, piece = random_move_value[0], random_move_value[1], random_piece
                
                    # Minimax algorithm
                    case 'minimax':
                        # Record the time
                        start_time_minimax = time()
                        (piece, action, jump), _ = MindMinimax.minimax(game=self, game_state=game_state, max_depth=models['minimax'],
                                                                    alpha=float('-inf'), beta=float('inf'))
                        end_time_minimax = time()
                        time_spent_minimax = end_time_minimax - start_time_minimax
                        
                        # Wait for remaining time if time_spent is less than 3 sec
                        if time_spent_minimax < 3.0:
                            sleep(3.0 - time_spent_minimax)
                            
                        # Get the original piece to prevent problems
                        original_pieces = self.pieces_dark if self.pieces_turn else self.pieces_light
                        for i in original_pieces:
                            if piece.id == i.id:
                                piece = i
                                
                    case 'q_learning':
                        sleep(2)
                        (piece, action, jump) = models['q_learning'].choose_action(state=self.board_to_tuple(), actions_pos=game_state[2])
                        
                    case 'deep_q_learning':
                        start_time_dql = time()
                        actions_list = [(piece, action, jump)
                                        for piece in sorted(game_state[2].keys(), key=lambda x: x.position)
                                        for action, jump in sorted(game_state[2][piece])]
                        action_number = models['deep_q_learning'].choose_action(np.append(self.board_to_tuple(), self.pieces_turn), actions_list)
                        (piece, action, jump) = actions_list[action_number]
                        end_time_dql = time()
                        time_spent_dql = end_time_dql - start_time_dql
                        
                        if time_spent_dql < 2.0:
                            sleep(2.0 - time_spent_dql)
                        
                    case _:
                        raise Exception('The AI model has been not found, play() cannot perform the operation')
                    
                # Make the move
                os.system('cls') if computer_system == 'Windows' else os.system('clear')
                self.make_move(action, jump, piece)  
                print(f'{ai_settings[0]} AI moved {piece} to {action}\n')
                                
                # Save the board
                self.board_history.append((self.board_to_tuple(), self.pieces_turn, self.pieces_counter))
                    
                # Prepare game for the next player
                self.pieces_turn = False if self.pieces_turn else True
                    
                game_state = tuple(self.game_over_conditions())
        
        # One AI against a human player
        elif any(self.ai_players[0]):
            # Depending on the input, the ai or the player starts
            ai_turn = True if self.ai_players[0][0] else False
            ai_kind = self.ai_players[1][0] if self.ai_players[1][0] is not None else self.ai_players[1][1]
            while game_state[0]:
                
                # AI turn
                if self.pieces_turn == ai_turn:
                    print('AI is making a move ...')
                    
                    match ai_kind:
                        
                        case 'random':
                            sleep(2)
                                
                            random_piece = random.choice(list(game_state[2].keys()))
                            random_move_value = random.choice(list(i for i in game_state[2][random_piece]))
                            action, jump, piece = random_move_value[0], random_move_value[1], random_piece
                        
                        case 'minimax':
                            # Record the time
                            start_time_minimax = time()
                            (piece, action, jump), _ = MindMinimax.minimax(game=self, game_state=game_state, max_depth=models['minimax'],
                                                                        alpha=float('-inf'), beta=float('inf'))
                            end_time_minimax = time()
                            time_spent_minimax = end_time_minimax - start_time_minimax
                            
                            # Wait for remaining time if time_spent is less than 3 sec
                            if time_spent_minimax < 2.0:
                                sleep(2.0 - time_spent_minimax)
                                
                            # Get the original piece to prevent problems
                            original_pieces = self.pieces_dark if self.pieces_turn else self.pieces_light
                            for i in original_pieces:
                                if piece.id == i.id:
                                    piece = i
                                    
                        case 'q_learning':
                            sleep(2)
                            (piece, action, jump) = models['q_learning'].choose_action(state=self.board_to_tuple(), actions_pos=game_state[2])
                            
                        case 'deep_q_learning':
                            start_time_dql = time()
                            actions_list = [(piece, action, jump)
                                            for piece in sorted(game_state[2].keys(), key=lambda x: x.position)
                                            for action, jump in sorted(game_state[2][piece])]
                            action_number = models['deep_q_learning'].choose_action(np.append(self.board_to_tuple(), self.pieces_turn), actions_list)
                            (piece, action, jump) = actions_list[action_number]
                            end_time_dql = time()
                            time_spent_dql = end_time_dql - start_time_dql
                            
                            if time_spent_dql < 2.0:
                                sleep(2.0 - time_spent_dql)
                        
                        case _:
                            raise Exception('The AI model has been not found, play() cannot perform the operation')

                    os.system('cls') if computer_system == 'Windows' else os.system('clear')
                    print(f'AI moved {piece} to {action}\n')
                        
                # Human turn
                else:
                    # Print the board and show all possible moves to the player
                    self.board_print()
                    print('')
                    id = 1
                    moves = []
                    for piece in sorted(game_state[2].keys()):
                        for action in sorted(game_state[2][piece]):
                            print(f'{id} --- {piece}: {action[0]}')
                            moves.append((piece, action))
                            id += 1
                    # Ask for the move to choose
                    while True:
                        print('')
                        try:
                            move_id = int(input("Please, choose the right move and type in it's id\n"))
                            if move_id in range(1, id):
                                break
                            else:
                                print(f'Id number out of range. Please, type in a number from 1 to {id - 1}')
                        except Exception as e:
                            print(e)
                            print(f'Please, try to type in a number from 1 to {id - 1}')
                    piece, move = moves[move_id - 1]
                    action, jump = move
                    
                # Make a move
                self.make_move(action, jump, piece)
                
                # Save the board
                self.board_history.append((self.board_to_tuple(), self.pieces_turn, self.pieces_counter))
                
                # Prepare game for the next player
                self.pieces_turn = False if self.pieces_turn else True

                game_state = tuple(self.game_over_conditions())
                
        # Two players game
        else:
            while game_state[0]:
                
                # Print the board and show all possible moves to the player
                self.board_print()
                print('')
                id = 1
                moves = []
                for piece in sorted(game_state[2].keys()):
                    for action in sorted(game_state[2][piece]):
                        print(f'{id} --- {piece}: {action[0]}')
                        moves.append((piece, action))
                        id += 1
                    # Ask for the move to choose
                while True:
                    print('')
                    try:
                        move_id = int(input("Please, choose the right move and type in it's id\n"))
                        if move_id in range(1, id):
                            break
                        else:
                            print(f'Id number out of range. Please, type in a number from 1 to {id - 1}')
                    except Exception as e:
                        print(e)
                        print(f'Please, try to type in a number from 1 to {id - 1}')
                
                # Make a move
                piece, move = moves[move_id - 1]
                action, jump = move
                self.make_move(action, jump, piece)
                
                
                # Save and clear the board
                self.board_history.append((self.board_to_tuple(), self.pieces_turn, self.pieces_counter))
                sleep(1)
                os.system('cls') if computer_system == 'Windows' else os.system('clear')
                print('Dark', end=' ') if self.pieces_turn else print('Light', end=' ')
                print(f'player moved {piece} to {action}\n')
                
                # Prepare game for the next player
                self.pieces_turn = False if self.pieces_turn else True

                game_state = tuple(self.game_over_conditions())
                
        # Game's finished
        self.board_print()
        match game_state[1]:
            case -1:
                print('\nLight pieces won.\n')
            case 0:
                print('\nDraw.\n')
            case 1:
                print('\nDark pieces won.\n')
        return game_state[1]
    
    def single_move(self, models):
        """
        Use the right AI to make a single move on the board.
        Returns game_state[:2] if the game is finished, True if playable
        """
        game_state = self.game_over_conditions()
        
        # If the game has finished
        if not game_state[0]:
            return game_state[:2]
        
        # Get the right AI model
        ai_kind = self.ai_players[1][0] if self.pieces_turn else self.ai_players[1][1]
        
        match ai_kind:
            
            case 'random':
                random_piece = random.choice(list(game_state[2].keys()))
                random_move_value = random.choice(list(i for i in game_state[2][random_piece]))
                action, jump, piece = random_move_value[0], random_move_value[1], random_piece
                
            case 'minimax':
                (piece, action, jump), _ = MindMinimax.minimax(game=self, game_state=game_state, max_depth=models['minimax'],
                                                            alpha=float('-inf'), beta=float('inf'))
                # Get the original piece to prevent problems
                original_pieces = self.pieces_dark if self.pieces_turn else self.pieces_light
                for i in original_pieces:
                    if piece.id == i.id:
                        piece = i
                        
            case 'q_learning':
                (piece, action, jump) = models['q_learning'].choose_action(state=self.board_to_tuple(), actions_pos=game_state[2])
                
            case 'deep_q_learning':
                actions_list = [(piece, action, jump)
                                for piece in sorted(game_state[2].keys(), key=lambda x: x.position)
                                for action, jump in sorted(game_state[2][piece])]
                action_number = models['deep_q_learning'].choose_action(np.append(self.board_to_tuple(), self.pieces_turn), actions_list)
                (piece, action, jump) = actions_list[action_number]
                
            case _:
                raise Exception('The AI model has been not found, single_move() cannot perform the operation')
        
        # Make a move
        self.make_move(action, jump, piece)
        
        # Save the board
        self.board_history.append((self.board_to_tuple(), self.pieces_turn, self.pieces_counter))
        
        # Prepare game for the next player
        self.pieces_turn = False if self.pieces_turn else True

        game_state = self.game_over_conditions()
        
        # If the game has finished
        if not game_state[0]:
            return game_state[:2]
        return game_state
    
    def train(self, models):
        """
        AI plays against itself, printing only results.
        self.ai_player[0] must be both True
        self.ai_player[1] must be set
        """
        game_state = tuple(self.game_over_conditions())
        if not game_state[0]:
            return game_state[1]
        
        # Check how many AI is in the game
        # AI plays against itself
        if all(self.ai_players[0]):
            # Get the ai settings
            dark_ai = (self.ai_players[0][0], self.ai_players[1][0])
            light_ai = (self.ai_players[0][1], self.ai_players[1][1])
            
            while game_state[0]:
                
                ai_settings = ('Dark', dark_ai[1]) if self.pieces_turn else ('Light', light_ai[1])
                
                match ai_settings[1]:
                    
                    # AI makes always random moves
                    case 'random':
                        
                        random_piece = random.choice(list(game_state[2].keys()))
                        random_move_value = random.choice(list(i for i in game_state[2][random_piece]))
                        action, jump, piece = random_move_value[0], random_move_value[1], random_piece
                    
                    # Minimax algorithm
                    case 'minimax':
                        (piece, action, jump), _ = MindMinimax.minimax(game=self, game_state=game_state, max_depth=models['minimax'],
                                                                    alpha=float('-inf'), beta=float('inf'))
                        # Get the original piece to prevent problems
                        original_pieces = self.pieces_dark if self.pieces_turn else self.pieces_light
                        for i in original_pieces:
                            if piece.id == i.id:
                                piece = i
                                
                    # Q-learning algorithm
                    case 'q_learning':
                        (piece, action, jump) = models['q_learning'].choose_action(state=self.board_to_tuple(), actions_pos=game_state[2])
                        
                    case 'deep_q_learning':
                        actions_list = [(piece, action, jump)
                                        for piece in sorted(game_state[2].keys(), key=lambda x: x.position)
                                        for action, jump in sorted(game_state[2][piece])]
                        action_number = models['deep_q_learning'].choose_action(np.append(self.board_to_tuple(), self.pieces_turn), actions_list)
                        (piece, action, jump) = actions_list[action_number]
                        
                    case _:
                        raise Exception('The AI model has been not found, train() cannot perform the operation')
                    
                # Make the move
                self.make_move(action, jump, piece)  
                                
                # Save the board
                self.board_history.append((self.board_to_tuple(), self.pieces_turn, self.pieces_counter))
                    
                # Prepare game for the next player
                self.pieces_turn = False if self.pieces_turn else True
                    
                game_state = tuple(self.game_over_conditions())
        return game_state[1]
        
    # Make a move and update the board (optionally act on a copy)
    def make_move(self, move, jump, piece, board_c=None):
        
        if jump:
            
            # Delete the enemy piece, additional for loop, because possibility of multiple jums, and so
            # move is ((move)) or ((move_1), move_2)
            for single_move in move:
                row_eq = 1 if single_move[0] - piece.position[0] > 0 else -1
                col_eq =  1 if single_move[1] - piece.position[1] > 0 else -1
                temp_val = (piece.position[0] + row_eq, piece.position[1] + col_eq)
                
                if not board_c:
                    # If acting on a main board
                    if piece.king:
                        # A king may have a long jump, and so every en route square should be checked
                        while self.board[temp_val[0]][temp_val[1]] is None:
                            temp_val = (temp_val[0] + row_eq, temp_val[1] + col_eq)
                            
                    all_one_color_pieces = self.pieces_dark if piece.color == False else self.pieces_light
                    enemy_piece = self.board[temp_val[0]][temp_val[1]]
                    self.board[temp_val[0]][temp_val[1]] = None
                    all_one_color_pieces.remove(enemy_piece)
                    enemy_piece = None
                    self.pieces_counter -= 1
                    # Move
                    self.board[piece.position[0]][piece.position[1]] = None
                    self.board[single_move[0]][single_move[1]] = piece
                    piece.position = single_move
                        
                # If acting on a copy
                else:
                    if piece.king:
                        # A king may have a long jump, and so every en route square should be checked
                        while board_c[temp_val[0]][temp_val[1]] is None:
                            temp_val = (temp_val[0] + row_eq, temp_val[1] + col_eq)
                            
                    enemy_piece = board_c[temp_val[0]][temp_val[1]]
                    board_c[temp_val[0]][temp_val[1]] = None
                    enemy_piece = None
                    # Move
                    board_c[piece.position[0]][piece.position[1]] = None
                    board_c[single_move[0]][single_move[1]] = piece
                    piece.position = single_move
            
        else:
            if not board_c:
                self.board[piece.position[0]][piece.position[1]] = None
                self.board[move[0]][move[1]] = piece
                piece.position = move
            else:
                board_c[piece.position[0]][piece.position[1]] = None
                board_c[move[0]][move[1]] = piece
                piece.position = move
        
        # If the man reaches the farthes row forward, it becomes a king
        if not board_c:
            row_farthest_forward = self.height - 1 if piece.color == True else 0
        else:
            row_farthest_forward = len(board_c) - 1 if piece.color == True else 0
        if piece.position[0] == row_farthest_forward:
            piece.king = True
        if board_c:
            return board_c
        return 0
        
    def game_over_conditions(self):
        """
            The game has ended if:
            - a player has no valid moves (no pieces left or no valid moves) => the opposite player wins;
            - one king vs one king game => draw;
            - the same position repeats itself for the third time (not necessarily consecutive),
            with the same player having the move each time (threefold).
            When the game ends => returns (game_state=False, winner=1 or 0 or -1, possible_moves)
        """
        winner = 0
        possible_moves = self.set_possible_moves()
        
        if not possible_moves:
            # The opposite player wins
            # 1(True) <=> Dark, 0(False) <=> Light
            winner = -1 if self.pieces_turn else 1
            return (False, winner, possible_moves)
        
        if self.pieces_counter == 2 and len(self.pieces_dark) == len(self.pieces_light):
            for piece_dark, piece_light in zip(self.pieces_dark, self.pieces_light):
                if piece_dark.king and piece_light.king:
                    return (False, winner, None)
                
        # Min amount to threefold to happen
        if len(self.board_history) >= 9:
            
            # Update the board history to delete all unnecesary computations
            self.board_history = [position for position in self.board_history if position[2] == self.board_history[-1][2]]
            if len(self.board_history) >= 9:
                repetition_count = {}
            
                for position in self.board_history:
                
                # # Alternative approach, iterate over, only the most important should be checked => optimisation
                # if position[2] == self.board_history[-1][2]:
                    position_sh = (position[0], position[1])
                    if repetition_count.get(position_sh):
                        repetition_count[position_sh] += 1
                    else:
                        repetition_count[position_sh] = 1
                
                    if repetition_count[position_sh] >= 3:
                                return (False, winner, None)
                            
                # An optional check of pieces following right positions (no piece should ever stand on a white square)
                # some_counter = -1
                # for ind, square in enumerate(position[0]):
                #     if ind % 10 == 0:
                #         some_counter *= (-1)
                        
                #     if some_counter == 1:
                #         if ind % 2 == 0:
                #             if square != 'None':
                #                 raise Exception('A piece should not be there!')
                #     else:
                #         if ind % 2 != 0:
                #             if square != 'None':
                #                 raise Exception('A piece should not be there!')
                # print(position[2])
                # print(self.board_history[-1][2])
                
        # If still in game
        return (True, winner, possible_moves)
    
    # Convert numpy array to tuple with a simple representation
    def board_to_tuple(self, board=None):
        """
        Convert the board to a simple tuple representation of the game state.
        + or - means black or white
        1 or 2 means a man or a king
        """
        board_repr = []
        if board is None:
            board = self.board
            
        for row in board:
            for square in row:
                if square is None:
                    board_repr.append(0)
                    continue
                sign = 1 if square.color else -1
                board_repr.append(sign * 2) if square.king else board_repr.append(sign * 1)
        return tuple(board_repr)
    
    def board_print(self, board=None):
        """
        Print the board in a friendly way to a human.
        """
        if board == None:
            board = self.board
            nr_r = 0
        for row in board:
            print(nr_r, ' ', end='')
            for square in row:
                if square is None:
                    print('|   |', end='')
                elif square.color == True:
                    print(f'|d{square.id:02d}|', end='')
                else:
                    print(f'|l{square.id:02d}|', end='')
            nr_r += 1
            print('')
        print('   ', end='')
        for nr_c in range(0, board.shape[1]):
            print(f'  {nr_c}  ', end='')
        print('')
        return 0
    
    def to_dict(self):
        """
        Convert the game to a JSON serializable form
        """
        result = {}
        for key, value in self.__dict__.items():
            if key.startswith('__'):
                continue
            
            if isinstance(value, (np.ndarray, np.generic)):
                # temp = value.tolist()
                temp = []
                for row in value:
                    for item in row:
                        if isinstance(item, Piece):
                            temp.append(item.id)
                        else:
                            temp.append(item)
                value = temp
                            
            elif key == 'pieces_dark' or key == 'pieces_light':
                temp = []
                for item in value:
                    temp.append((
                        item.id,
                        item.color,
                        item.position,
                        item.king
                    ))
                value = temp
                
            result[key] = value
        return result
        
    
class Piece():
    
    def __init__(self, id, color, position=None, king=False):
        self.id = id
        self.color = color
        self.position = position
        self.king = king
    
    def __repr__(self):
        return f'{self.id}_{"light" if not self.color else "dark"}'
    
    def __lt__(self, other):
        # Define the comparison logic based on the 'id' attribute
        return self.id < other.id
