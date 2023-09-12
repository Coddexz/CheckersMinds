from copy import deepcopy
import random


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


class MindMinimax:
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
                
                if square is None:
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
            
    
class MindQLearning:
    
    def __init__(self, q=None, alpha_min=0.01, alpha_max=0.8, alpha_dec=0.9995, gamma=0.7, eps_min=0.01, eps_max=1.0, eps_dec=0.9995):
        """"
        Initialise AI with an empty q-learning dictionary,
        an alpha (learning rate), gamma (discount factor) and epsilon rate.
        Epsilon and alpha both have a max point, a decay rate, and a min point.
        
        The q-learning dict maps (state, action) pairs to a q-value (a number).
            - state is a tuple composed of values e.g. (0, 1, 1, 1 ...) details => Checkers.board_to_tuple()
            - action is a tuple composed of a piece, a move, and a boolean for
            jumping over an enemy piece, e.g. action=(0_dark, (4, 3), False)
        """
        if not q:
            self.q = dict()
        else:
            self.q = q
        self.alpha_min = alpha_min
        self.alpha_max = alpha_max
        self.alpha_dec = alpha_dec
        self.alpha = self.alpha_max
        self.gamma = gamma
        self.eps_min = eps_min
        self.eps_max = eps_max
        self.eps_dec = eps_dec
        self.epsilon = self.eps_max
        
    def update_q_value(self, state, action, new_state, new_actions, reward):
        """
        Update q table for a specific state-action pair using the q table update rule.
        """
        # Update with the Q table rule
        # Q(s, a) = Q(s, a) + α * [R(s, a) + γ * max(Q(s', a')) - Q(s, a)]
        old_q = self.get_q_value(state, action)
        max_future_q = self.best_future_reward(new_state, new_actions)
        old_q += self.alpha * (reward + self.gamma * max_future_q - old_q)
        return 0
    
    def best_future_reward(self, state, actions):
        """
        Given a state, consider all possible `(state, action)` pairs available in that state and
        return the maximum of all of their Q-values.

        Use 0 as the Q-value if a `(state, action)` pair has no
        Q-value in `self.q`.
        """
        if not actions:
            return 0
        best_fut_result = float('-inf')
        
        for k, v in actions.items():
            for move in v:
                action = (k, move[0], move[1])
                q_value = self.get_q_value(state, action)
                if q_value > best_fut_result:
                    best_fut_result = q_value
        return best_fut_result
    
    def get_q_value(self, state, action):
        # Get q_value from the dict, if does not exist => return 0
        return self.q.setdefault((state, action), 0)

    def choose_action(self, state, actions_pos):
        """
        Given a state and actions possible, return an action to take.
        action = (piece, (move), jump)
        The same q value means any of options is an acceptable return value
        """
        
        if len(actions_pos) == 1:
            for k, v in actions_pos.items():
                for i in v:
                    return (k, i[0], i[1])
        else:
            q_value_max, action_to_choose = float('-inf'), None
            
            # Random action or the best known => epsilon decides
            random_action = random.choices(population=(True, False),cum_weights=(self.epsilon, 1))[0]
            if not random_action:
                for k, v in actions_pos.items():
                    for move in v:
                        action = (k, move[0], move[1])
                        q_value = self.get_q_value(state, action)
                        if q_value >= q_value_max:
                            if q_value > q_value_max:
                                q_value_max = q_value
                                action_to_choose = action
                            else:
                                action_to_choose = random.choice((action_to_choose, action))
            else:
                all_actions = [(k, move[0], move[1]) for k, v in actions_pos.items() for move in v]
                action_to_choose = random.choice(all_actions)
                        
        return action_to_choose
    
    def train(self, game):
        """
        Train the q_learning model
        """
        # Get the game state => returns (game_state=False, winner=1 or 0 or -1, possible_moves)
        # if the game's finished
        game_state = game.game_over_conditions()
        
        # Keep track of last move made by either player
        # 0 => Light
        # 1 => Dark
        last = {
            0: {'state': None, 'action': None, 'reward': None, 'next_actions': None},
            1: {'state': None, 'action': None, 'reward': None, 'next_actions': None}
        }
        
        # Game loop
        while game_state[0]:
            # Get moves, tupled copy of the board, and pieces to compare
            state = game.board_to_tuple()
            actions = game_state[2]
            state_value = MindMinimax.utility(game.board)
            
            # Let the AI select the best action
            action = self.choose_action(state=state, actions_pos=actions)
            
            # Keep track of last state and action
            last[game.pieces_turn]['state'] = state
            last[game.pieces_turn]['action'] = action
            
            # Make move on the board, check next possible actions and store them
            game.make_move(move=action[1], jump=action[2], piece=action[0])
            next_actions = game.set_possible_moves()
            last[game.pieces_turn]['next_actions'] = next_actions
            
            # Get reward for move and store it
            reward = abs(MindMinimax.utility(game.board)) - abs(state_value)
            last[game.pieces_turn]['reward'] = reward
            
            # Save board and prepare game for the next player
            game.board_history.append((game.board_to_tuple(), game.pieces_turn, game.pieces_counter))
            game.pieces_turn = False if game.pieces_turn else True
            
            # Check the state of the game
            game_state = game.game_over_conditions()
            
            # Update q_value for the current player and for the last player
            if game_state[1] == 0:
                self.update_q_value(state=state, action=action, new_state=game.board_to_tuple(),
                                new_actions=next_actions, reward=reward)
                if last[game.pieces_turn]['state'] is not None:
                    self.update_q_value(state=last[game.pieces_turn]['state'], action=last[game.pieces_turn]['action'],
                                    new_state=state, new_actions=last[game.pieces_turn]['next_actions'], reward=last[game.pieces_turn]['reward'] - reward)
            else:
                self.update_q_value(state=state, action=action, new_state=game.board_to_tuple(),
                                new_actions=next_actions, reward=GAME_WON + reward)
                self.update_q_value(state=last[game.pieces_turn]['state'], action=last[game.pieces_turn]['action'],new_state=state,
                                    new_actions=last[game.pieces_turn]['next_actions'], reward=last[game.pieces_turn]['reward'] - GAME_WON - reward)
            
        # Change epsilon
        if self.epsilon > self.eps_min:
            self.epsilon *= self.eps_dec
        # Change alpha
        if self.alpha > self.alpha_min:
            self.alpha *= self.alpha_dec