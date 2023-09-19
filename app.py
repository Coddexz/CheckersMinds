from flask import Flask, jsonify
from game.checkers import Checkers


app = Flask('__name__')


# Generate index template (React)
@app.route('/')
def index():
    return '<h1>Hello World</h1>'

# Initialise a default game and send it back as a json object
@app.route('/game/init')
def game_init():
    game = Checkers()
    return jsonify(game.to_dict())


if __name__ == '__main__':
    app.run(debug=True)