from game.checkers import Checkers
from game.minds import MindDeepQLearning
import os
import time


DEEP_Q_LEARNING_TIME_LIMIT = 4
DEEP_Q_LEARNING_MODEL_DIR = os.path.join(os.getcwd(),'game', 'sm_ind_rew_repc_3r_2dr')
DEEP_Q_LEARNING_MODEL_DIR_SAVE = os.path.join(os.getcwd(), 'game', 'sm_ind_rew_repc_3r_2dr_xx')


def main():
    time_start = time.time()
    deep_counter = 0
    
    if not os.path.exists(DEEP_Q_LEARNING_MODEL_DIR):
        
        ai_deep_q_learning = MindDeepQLearning(input_length=len(Checkers().board_to_tuple()) + 3,
                                            max_output_len=Checkers().pieces_counter)
        
        while True:
            if ai_deep_q_learning.train_counter == 0:
                ai_deep_q_learning.model_save(f"{DEEP_Q_LEARNING_MODEL_DIR_SAVE}_emg")
            print(f'{deep_counter + 1} training game')
            game = Checkers()
            ai_deep_q_learning.play(game=game)
            elapsed_time = time.time() - time_start
            deep_counter += 1
            if elapsed_time >= 1800 * DEEP_Q_LEARNING_TIME_LIMIT:
                break
        ai_deep_q_learning.model_save(DEEP_Q_LEARNING_MODEL_DIR_SAVE)
        print(f'Model saved to {DEEP_Q_LEARNING_MODEL_DIR_SAVE}')
        print(deep_counter)
            
    else:
        ai_deep_q_learning = MindDeepQLearning(input_length=len(Checkers().board_to_tuple()) + 3,
                                                max_output_len=Checkers().pieces_counter,
                                                model_path=DEEP_Q_LEARNING_MODEL_DIR)
        print(f'Deep Q-learning model loaded. Path: {DEEP_Q_LEARNING_MODEL_DIR}')
        time.sleep(5)
        
        while True:
            if ai_deep_q_learning.train_counter == 0:
                ai_deep_q_learning.model_save(f"{DEEP_Q_LEARNING_MODEL_DIR_SAVE}_emg")
            print(f'{deep_counter + 1} training game')
            game = Checkers()
            ai_deep_q_learning.play(game=game)
            elapsed_time = time.time() - time_start
            deep_counter += 1
            if elapsed_time >= 1800 * DEEP_Q_LEARNING_TIME_LIMIT:
                break
        ai_deep_q_learning.model_save(DEEP_Q_LEARNING_MODEL_DIR_SAVE)
        print(f'Model saved to {DEEP_Q_LEARNING_MODEL_DIR_SAVE}')
        print(deep_counter)
        
if __name__ == '__main__':
    main()