from game.checkers import Checkers
from game.minds import MindDeepQLearning
import os
import time


DEEP_Q_LEARNING_TIME_LIMIT = 3
DEEP_Q_LEARNING_MODEL_DIR = os.path.join(os.getcwd(), 'backend', 'game', 'deep_q_model')
DEEP_Q_LEARNING_MODEL_DIR_SAVE = os.path.join(os.getcwd(), 'backend', 'game', 'deep_q_model')


def main():
    time_start = time.time()
    deep_counter = 0
    
    if not os.path.exists(DEEP_Q_LEARNING_MODEL_DIR):
        
        ai_deep_q_learning = MindDeepQLearning(input_length=len(Checkers().board_to_tuple()) + 1,
                                            max_output_len=Checkers().pieces_counter,
                                            target_update_interval=23)
        
        while True:
            print(f'{deep_counter + 1} training game')
            game = Checkers()
            ai_deep_q_learning.play(game=game)
            elapsed_time = time.time() - time_start
            deep_counter += 1
            if elapsed_time >= 1800 * DEEP_Q_LEARNING_TIME_LIMIT:
                break
        ai_deep_q_learning.epsilon = -1
        ai_deep_q_learning.model_save(DEEP_Q_LEARNING_MODEL_DIR_SAVE)
        print('Model saved')
        print(deep_counter)
            
    else:
        ai_deep_q_learning = MindDeepQLearning(input_length=len(Checkers().board_to_tuple()) + 1,
                                                max_output_len=Checkers().pieces_counter,
                                                target_update_interval=23,
                                                model_path=DEEP_Q_LEARNING_MODEL_DIR)
        print('Deep Q-learning model loaded')
        time.sleep(5)
        ai_deep_q_learning.epsilon = 0.6
        
        while True:
            print(f'{deep_counter + 1} training game')
            game = Checkers()
            ai_deep_q_learning.play(game=game)
            elapsed_time = time.time() - time_start
            deep_counter += 1
            if elapsed_time >= 1800 * DEEP_Q_LEARNING_TIME_LIMIT:
                break
        ai_deep_q_learning.epsilon = -1
        ai_deep_q_learning.model_save(DEEP_Q_LEARNING_MODEL_DIR_SAVE)
        print('Model saved')
        print(deep_counter)
        
if __name__ == '__main__':
    main()