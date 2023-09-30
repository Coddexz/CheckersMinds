import React, { useState, useMemo } from "react";

const CheckersContainer = (props) => {

  const seePossibleMoves = (event) => {
    let eventShort = event.props.children
    const value = {
      ID: eventShort[1],
      Color: eventShort[3],
      Position: eventShort[5],
      King: eventShort[7]
    }

    let squaresToHighlightArray = []

    // Get the range of ids within the ooposite colour
    let maxPlayerPieces = ((props.game.height - 2) / 2) * (props.game.width / 2)
    let minPlayerPieces = 0
    // Correct if light pieces
    if (value.Color) {
      minPlayerPieces = maxPlayerPieces
      maxPlayerPieces *= 2
    }

    if (value.King) {
      //pass
    } else {
    let moveRange = [-1, 1]
    for (let moveVertical of moveRange) {
      let VerticalNewPos = value.Position[0] + moveVertical
      if (VerticalNewPos < 0 || VerticalNewPos > props.game.height) continue
      for (let moveHorizontal of moveRange) {
        let HorizontalNewPos = value.Position[1] + moveHorizontal
        if (HorizontalNewPos < 0 || HorizontalNewPos > props.game.width) continue

        let positionToCheckStr = VerticalNewPos.toString() + HorizontalNewPos

        if (props.game.board[parseInt(positionToCheckStr)] === null) {
          squaresToHighlightArray.push([parseInt(positionToCheckStr[0]), parseInt(positionToCheckStr[1]), value])

        } else if (minPlayerPieces <= props.game.board[parseInt(positionToCheckStr)] &&
        props.game.board[parseInt(positionToCheckStr)] < maxPlayerPieces) {
          // If the piece belongs to the opposite colour
          let squareBehindEnemy = (parseInt(positionToCheckStr[0]) + moveVertical).toString() +
          (parseInt(positionToCheckStr[1]) + moveHorizontal).toString()

          if (props.game.board[parseInt(squareBehindEnemy)] === null) {
            squaresToHighlightArray.push([parseInt(squareBehindEnemy[0]), parseInt(squareBehindEnemy[1]), value])
          }

        } else continue
        }
        }
        // Highlight all fields
        setSquaresToHighlight(squaresToHighlightArray)
      }
    }

  const makeMove = (pieceToMove, highlightedPosition) => {
    /*
    Make a move on the board, i.e. change board, change, pieces
    If there are possible further jumping moves =>
    highlight squares and repeat make move till there is not any possible move left
    
    Save the board in board_history
    Prepare the game fo the next player => change pieces_turn and check if the game has ended
    */
    console.log(pieceToMove)
    console.log(highlightedPosition)
    let highlightedPositionStr = highlightedPosition[0].toString() + highlightedPosition[1]

  }

  const generateTable = () => {
    const table = [];

    for (let i = 0; i < props.game.height; i++) {
      const row = [];
      for (let j = 0; j < props.game.width; j++) {
        let cellClass = ''
        let cellContent = null
        let cellImage = null
        let cellClick = undefined

        if ((i % 2 === 0 && j % 2 === 0) || (i % 2 !== 0 && j % 2 !== 0)) {
          cellClass = 'empty-square'
          cellClick = () => setSquaresToHighlight([])
        } else {
          cellClass = 'func-square'
          for (let piece of props.game.pieces_dark) {
            if (piece[2][0] === i && piece[2][1] === j) {
              cellContent = (
                <>
                  ID : {piece[0]}, Color: {piece[1]}, Position: {piece[2]}, King: {piece[3]}
                </>
              );
              if (piece[3]) {
                cellImage = <img src="/dark_piece_king.png" alt="Dark Piece King" />
            } else {
                cellImage = <img src="/dark_piece.png" alt="Dark Piece" />
            }
              break;
            }
          }

          if (!cellContent) {
            for (let piece of props.game.pieces_light) {
              if (piece[2][0] === i && piece[2][1] === j) {
                cellContent = (
                  <>
                    ID : {piece[0]}, Color: {piece[1]}, Position: {piece[2]}, King: {piece[3]}
                  </>
                );
                if (piece[3]) {
                    cellImage = <img src="/light_piece_king.png" alt="Light Piece King" />
                } else {
                    cellImage = <img src="/light_piece.png" alt="Light Piece" />
                }
                break;
              }
            }
          }
          /* If this is a piece, it is a current human player turn, and the piece belongs to the
          current player, cellContent.props.children[3] == Colour of the cellContent*/
          let pieces_turn = props.game.pieces_turn ? 1 : 0
          if (cellContent && !props.game.ai_players[0][pieces_turn] &&
            cellContent.props.children[3] === props.game.pieces_turn) {
            cellClick = () => seePossibleMoves(cellContent)
          } else cellClick = () => setSquaresToHighlight([])
          // Highlight squares if array squaresToHighlight exists
          if (squaresToHighlight) {
            for (let squarePosition of squaresToHighlight) {
              if (squarePosition[0] === i && squarePosition[1] === j) {
                cellClass = 'func-square highlighted-square'
                cellClick = () => makeMove(squarePosition[2], [squarePosition[0], squarePosition[1]])
              }
            }
          }
        }
        row.push(
          <td key={j} className={cellClass} value={cellContent} onClick={cellClick}>
            {cellImage}
          </td>
        );
      }
      table.push(<tr key={i}>{row}</tr>)
    }
    return table
  }

  const [squaresToHighlight, setSquaresToHighlight] = useState([])
  const generateCheckers = useMemo(() => generateTable(squaresToHighlight), [squaresToHighlight])

  return (
    <div id="game-container">
      <div>{JSON.stringify(props.game)}</div>
      <table>
        {/* <tbody>{generateTable()}</tbody> */}
        <tbody>{generateCheckers}</tbody>
      </table>
    </div>
  )
}

export default CheckersContainer