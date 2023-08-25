from copy import deepcopy


"""
Rewards for different types of activities during the game.
Light pieces get negative value.
Pieces get points by being on the edge on of the board.
Being closer to the enemy top of the board means one additional point counted from the middle row of the board.
"""
GAME_WON = 100
OWN_PIECE = 5
OWN_KING = 10
OWN_PIECE_ON_EDGE = 2
OWN_PIECE_CLOSER_TOP = 1


class MindMinimax():
    """
    Representation of an minimax algorithm with alpha beta pruning.
    Returns the optimal action for the current player on the board.
    The action is optimal for n moves in the game to make it more effiecent.
    """
    
    @staticmethod
    def utility(board):
        """
        Returns utility for the state
        """
        # Prepare variables
        height, width = board.shape
        pieces, kings, position_edge, position_top = 0, 0, 0, 0
        row_no_value = height // 2
        
        for row in range(0, height):
            for col in range(0, width):
                square = board[row][col]
                
                if square == None:
                    continue
                
                # Dark pieces
                if square.color:
                    # Points based on the piece characteristic
                    if square.king:
                        kings += 1
                    else:
                        pieces += 1
                        
                    # Points based on the piece position
                    if col == 0 or col == width - 1:
                        position_edge += 1
                    
                    if row >= row_no_value:
                        for index, item in enumerate(range(row_no_value, height, 1)):
                            if row == item:
                                position_top += index
                            
                # Light pieces
                else:
                    # Points based on the piece characteristic
                    if square.king:
                        kings -= 1
                    else:
                        pieces -= 1
                        
                    # Points based on the piece position
                    if col == 0 or col == width - 1:
                        position_edge -= 1

                    if row < row_no_value:
                        for index, item in enumerate(range(row_no_value - 1, -1, -1)):
                            if row == item:
                                position_top -= index
                                
        return pieces * OWN_PIECE + kings * OWN_KING + position_edge * OWN_PIECE_ON_EDGE + position_top * OWN_PIECE_CLOSER_TOP
  
    @staticmethod
    def minimax(game, game_state, max_depth, alpha, beta, cur_depth=0):
        """
        Minimax alghorhytm with alpha beta prunning
        Returns an optimal action for the current player on the board
        """

        # Do not proceed if the game is finished, return the action and its utility
        if not game_state[0] or cur_depth == max_depth:
            if not game_state[0]:
                if game_state[1] == 1:
                    next_state_utility = GAME_WON
                elif game_state[1] == 0:
                    next_state_utility = 0
                else:
                    next_state_utility = - GAME_WON
            else:
                next_state_utility = MindMinimax.utility(game.board)

            return None, next_state_utility
        
        # Maximising player's turn
        if game.pieces_turn:
            best_utility = float('-inf')
            
            # Choose an action to evaluate its score
            for piece in game_state[2].keys():
                for action, jump in game_state[2][piece]:
                    
                    # Copy the object
                    game_copy = deepcopy(game)
                    # Get the copied piece to prevent problems
                    copied_pieces = game_copy.pieces_dark if game.pieces_turn else game_copy.pieces_light
                    for i in copied_pieces:
                        if piece.id == i.id:
                            piece = i
                    
                    # Make the move on the copy and save
                    game_copy.make_move(action, jump, piece)
                    game_copy.board_history.append((game_copy.board_to_tuple(), game_copy.pieces_turn,game_copy.pieces_counter))
                    game_copy.pieces_turn = False if game_copy.pieces_turn else True
                    
                    # Check the state of the game
                    game_copy_state =tuple(game_copy.game_over_conditions())
                    
                    _, utility = MindMinimax.minimax(game_copy, game_copy_state, max_depth, alpha, beta, cur_depth + 1)

                    # Choose the best action
                    if utility > best_utility:
                        best_utility = utility
                        best_action = (piece, action, jump)
                    
                    # Beta cutoff, if there is no option that this will be choosen
                    alpha = max(alpha, best_utility)
                    if beta <= alpha:
                        break
                    
        # Minimasing player's turn
        else:
            best_utility = float('inf')
            
            # Choose an action to evaluate its score
            for piece in game_state[2].keys():
                for action, jump in game_state[2][piece]:
                    
                    # Copy the object
                    game_copy = deepcopy(game)
                    # Get the copied piece to prevent problems
                    copied_pieces = game_copy.pieces_dark if game.pieces_turn else game_copy.pieces_light
                    for i in copied_pieces:
                        if piece.id == i.id:
                            piece = i
                    
                    # Make the move on the copy and save
                    game_copy.make_move(action, jump, piece)
                    game_copy.board_history.append((game_copy.board_to_tuple(), game_copy.pieces_turn,game_copy.pieces_counter))
                    game_copy.pieces_turn = False if game_copy.pieces_turn else True
                    
                    # Check the state of the game
                    game_copy_state =tuple(game_copy.game_over_conditions())
                    
                    _, utility = MindMinimax.minimax(game_copy, game_copy_state, max_depth, alpha, beta, cur_depth + 1)

                    # Choose the best action
                    if utility < best_utility:
                        best_utility = utility
                        best_action = (piece, action, jump)
                    
                    # Beta cutoff, if there is no option that this will be choosen
                    beta = min(beta, best_utility)
                    if beta <= alpha:
                        break

        return best_action, best_utility
            
        