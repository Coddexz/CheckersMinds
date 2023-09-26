import React from "react";

const RulesContainer = (props) => {

    const handleClick = () => {
        props.setShowRules(false)
    }
  return (
    <div id="rules">
      <h1>Checkers Rules</h1>

      <ul>
        <li>International checkers is played on a 10x10 board with 20 pieces per player.</li>
        <li>Pieces can move diagonally one square forward or backward.</li>
        <li>
          When a piece spots an enemy, it can jump over it if there is an empty
          square behind it. This eliminates the opponent's piece. If possible,
          the piece can make several jumps over an enemy piece.
        </li>
        <li>If there is an option to jump over an enemy piece, you must do so.</li>
        <li>You do not have to choose always the biggest number of jumps.</li>
        <li>If a piece reaches the opposite first row, it becomes a king.</li>
        <li>
          A king is not limited by number of squares, it can move and jump over
          as many squares as he wants as long as it is a diagonal move.
        </li>
        <li>
          A king can jump over an enemy piece in the same way as a normal piece.
          The only difference is that he can choose to move to another square if
          it is empty.
        </li>
        <li>The game is won when the other player has no more possible moves or no
        more pieces or kings.</li>
        <li>It works the other way round, if you run out of moves, you lose.</li>
        <li>The game ends in a draw if there is a King vs. King game, or if the same
        position is repeated for the third time (not necessarily consecutively),
        with the same player having the move each time (threefold).</li>
      </ul>
      <div>
        <button type="button" onClick={handleClick} id="rules-button">
            Go back
        </button>
      </div>
    </div>
  );
};

export default RulesContainer;