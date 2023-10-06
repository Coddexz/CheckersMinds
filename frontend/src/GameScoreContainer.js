import React from "react"

const GameScoreContainer = (props) => {
    let winner = undefined
    switch (props.winner) {
        case -1:
            winner = 'The light pieces won.'
            break

        case 0:
            winner = 'Draw.'
            break

        case 1:
            winner = 'The dark pieces won.'
            break

        default:
            throw new Error('{GameScoreContainer} The winner has been not found')
    }

    return (
        <div id="score">
            Game over. {winner}
        </div>
    )
}

export default GameScoreContainer