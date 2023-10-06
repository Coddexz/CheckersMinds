# Checkers Minds
Checkers Minds is a two-player board game of checkers that can be played by humans or AIs. It is a turn-based game where players take turns moving their pieces across the board, capturing their opponent's pieces as they go. The goal of the game is to be the first player to capture all of their opponent's pieces or to leave them with no legal moves.

Checkers Minds has two versions:
  * **Frontend**: This version of the game is written in React and Flask, and it features a graphical user interface where players can move their pieces by clicking on them.
  * **Terminal**: This version of the game is written in Python, and it has a simplified text-based interface where players enter commands to move their pieces.


## Features
* Supports both human and AI players
* Four AI models: random, minimax, q-learning, and deep q-learning
* Can be played in training mode, where the AIs play against each other without showing every move (only the final score after playing the selected number of games)
* Should support a variety of board sizes (default is 10x10)

## Getting Started
To play Checkers Minds, first install the dependencies in the `backend` directory:
 * using pipenv:
   `pipenv install`
 * using pip:
  `pip install -r requirements.txt`

If you are using the frontend version of the game, you will also need to install the dependencies in the `frontend` directory:\
  `npm install`

Once you have installed the dependencies, you can start the game by running the following commands:\
  `npm start` in `frontend`\
  `python server.py` in `backend`

You can also run the game directly from the `checkers_minds_play.py` file.


### Usage
When the game starts, you will be prompted to select the type of game you want to play. You can choose between:
* AI vs AI (training)
* AI vs AI
* Human vs AI
* AI vs Human
* Human vs Human

Once you have selected a game type, you will be prompted to select the AI models for the AI players. You can choose from:
* random
* minimax
* q-learning (not functional in frontend)
* deep_q_learning

If you are playing a Human vs Human game, you will be able to take turns moving your pieces. After running the file, the exact rules of the game will be explained.

### Training (Terminal version)
If you wish to use the AI models in the training mode, you can do so by selecting the AI vs AI (training) game type. You will then be asked to enter the number of training games you want the AIs to play.

The AIs will play a series of games against each other. Once the training is complete, you will be able to see how the AI performed in the game.

### Licence
Checkers Minds is released under the MIT Licence.

### Troubleshooting
If you are having problems with the performance of the minimax algorithm, you can try changing the `MINIMAX_MAX_DEPTH` variable in `server.py` or `checkers_minds_play.py`. This variable controls the number of moves that the minimax algorithm looks ahead. A higher value will give the algorithm more information to work with, but it will also make the algorithm slower.

Please note that Q-learning requires significant computational power and may not work effectively without access to high-performance hardware. You can modify the number of stored games by changing `Q_LEARNING_TRAINING_GAMES` in `checkers_minds_play.py`.

The Deep Q-learning model is available in the GitHub folder. You can train your own model by deleting or renaming the existing `deep_q_model` in the `backend/game` directory. Adjust the training time using `DEEP_Q_LEARNING_TIME_LIMIT` in `checkers_minds_play.py`, where 1 unit represents 30 minutes. You can also enable additional training by changing the `TRAIN_MORE_DEEP_Q` option.

Deep Q-learning is functional, though it benefits from further optimization, which demands ample time, computational resources, rigorous testing, and a richer dataset of games played.

Enjoy your games with Checkers Minds!