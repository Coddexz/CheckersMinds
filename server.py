from flask import Flask, jsonify, request
from flask_cors import CORS
from game.checkers import Checkers


app = Flask('__name__')
CORS(app)


# Initialise a default game and send it back as a json object
@app.route('/game/init', methods=['POST'])
def game_init():
    
    data = request.json
    print(data)
    game = Checkers()
    return jsonify(game.to_dict())


if __name__ == '__main__':
    app.run(debug=True)