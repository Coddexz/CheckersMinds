import React, { useState, useEffect } from "react";

const CheckersContainer = (props) => {

  const makeMove = (pieceToMoveId, highlightedPosition, jump) => {
    /*
    In React:
    Make a move on the board, i.e. change board, change, pieces
    If there are possible further jumping moves =>
    highlight squares and repeat make move till there is not any possible move left
    In Flask:
    Save the board in board_history
    Prepare the game fo the next player => change pieces_turn and check if the game has ended
    */

    let pieceToMove = undefined
    console.log(pieceToMoveId)

    for (const piece of props.game.pieces_dark) {
      if (piece[0] === pieceToMoveId) {
        pieceToMove = piece
        break
      }
    }
    if (!pieceToMove) {
      for (const piece of props.game.pieces_light) {
        if (piece[0] === pieceToMoveId) {
          pieceToMove = piece
          break
        }
      }
    }
    console.log(pieceToMove)
    console.log(highlightedPosition)
    setFirstMove(false)
    let boardToUpdate = undefined
    let highlightedPositionStr = highlightedPosition[0].toString() + highlightedPosition[1]

    // Change the board object
    let boardObject = [...props.game.board]
    boardObject[parseInt(highlightedPositionStr)] = pieceToMove.id
    boardObject[parseInt(pieceToMove.Position[0].toString() + pieceToMove.Position[1])] = null

    // Change pieces counter and array
    let piecesArr = pieceToMove.Color ? [...props.game.pieces_dark] : [...props.game.pieces_light]
    // To be continued, it doesn't change the value of piece in the array!!!
    for (const [i, piece] of piecesArr.entries()) {
      if (piece[0] === pieceToMove.ID) {
        piecesArr[i][2] = [highlightedPosition[0], highlightedPosition[1]]
      }
    }

    if (jump) {
      let newPiecesCounter = props.game.pieces_counter - 1

      // Check the enemy position
      const heightEqualizer = (highlightedPosition[0] - pieceToMove.Position[0]) > 0 ? 1 : -1
      const widthEqualizer = (highlightedPosition[1] - pieceToMove.Position[1]) > 0 ? 1 : -1

      let enemyPieceHeight = pieceToMove.Position[0]
      let enemyPieceWidth = pieceToMove.Position[1]
      
      while (true) {
        if ((enemyPieceHeight + heightEqualizer) === highlightedPosition[0]) break
        enemyPieceHeight += heightEqualizer
        enemyPieceWidth += widthEqualizer
      }

      let enemyPiecePosStr = enemyPieceHeight.toString() + enemyPieceWidth
      console.log(enemyPiecePosStr)
      boardObject[parseInt(enemyPiecePosStr)] = null

      let enemyPiecesArr = pieceToMove.Color ? [...props.game.pieces_light] : [...props.game.pieces_dark]
      console.log(enemyPiecesArr, 'enemy pieces array')
      for (let i = 0; i < enemyPiecesArr.length; i++) {
        if (enemyPiecesArr[i][2][0] === enemyPieceHeight && enemyPiecesArr[i][2][1] === enemyPieceWidth) {
          console.log('enemy:')
          console.log(enemyPiecesArr[i])
          enemyPiecesArr.splice(i, 1)
        }}
      boardToUpdate = {
        'board': boardObject,
        'pieces_counter': newPiecesCounter,
        [pieceToMove.Color ? 'pieces_dark' : 'pieces_light']: piecesArr,
        [pieceToMove.Color ? 'pieces_light' : 'pieces_dark']: enemyPiecesArr,
      }
      } else {
        boardToUpdate = {
          'board': boardObject,
          [pieceToMove.Color ? 'pieces_dark' : 'pieces_light']: piecesArr,
        }
      }
      console.log('Before setting squaresToHighlight:', squaresToHighlight);
    // Empty squares
    // setSquaresToHighlight([])
      // Debugging
  console.log('After setting squaresToHighlight:', squaresToHighlight);

    // If the piece crossed reached the end of the board => make it a king
    if ((pieceToMove.Color && highlightedPosition[0] == (props.game.height - 1)) ||
    (!pieceToMove.Color && highlightedPosition[0] == 0)) {
      for (const [i, piece] of piecesArr.entries()) {
        if (piece[0] === pieceToMove.ID) {
          piecesArr[i][3] = true
        }
      }
      boardToUpdate = {...boardToUpdate, [pieceToMove.Color ? 'pieces_dark' : 'pieces_light']: piecesArr,}
    }
    // Save the game state
    props.setGame({...props.game, ...boardToUpdate})

    for (const piece of piecesArr) {
      if (piece[0] === pieceToMove.ID) {
        pieceToMove = {'ID': piece[0], 'Color': piece[1], 'Position': piece[2], 'King': piece[3]}
      }
    }
    
    // If this piece can make any other moves -> highlight position and allow for making only them
    if (jump) {
      // seePossibleMoves(pieceToMove, true)
    }

    sendGame(props.game)
    return
  }
  const sendGame = (gameToSend) => {
      // Make a fetch request to the `/game/move` endpoint.
      // const data = JSON.stringify({...props.gameInitData, players: convertPlayers(props.gameInitData.players)})

      fetch("http://127.0.0.1:5000/game/move", {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({
              ...gameToSend,
          })
      })
      .then((res) => {
          if (!res.ok) {
              throw new Error('Network response was not ok')
          }
          return res.json();
      })
      .then((checkersGame) => {
          // Set the checkersGame state with the JSON response.
          props.setGame(checkersGame)
      })
      .catch((err) => {
          // Handle errors and show a user-friendly message.
          console.error('Error:', err);
          alert('An error occurred while fetching the game data.')
      })
      setFirstMove(true)
      // setSquaresToHighlight([0])
  }

  const generateTable = () => {
    const board = []
    for (let i = 0; i < props.game.height; i++) {
      const row = [];
      for (let j = 0; j < props.game.width; j++) {
        let cellClass = undefined
        let cellContent = undefined
        let cellImage = null
        let cellClick = null

        if ((i % 2 === 0 && j % 2 === 0) || (i % 2 !== 0 && j % 2 !== 0)) {
          cellClass = 'empty-square'
          if (firstMove) cellClick = () => setSquaresToHighlight([])
        } else {
          cellClass = 'func-square'
          for (let piece of props.game.pieces_dark) {
            if (piece[2][0] === i && piece[2][1] === j) {
              cellContent = {id: piece[0], color: piece[1], position: piece[2], king: piece[3]}
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
                cellContent = {id: piece[0], color: piece[1], position: piece[2], king: piece[3]}
                if (piece[3]) {
                    cellImage = <img src="/light_piece_king.png" alt="Light Piece King" />
                } else {
                    cellImage = <img src="/light_piece.png" alt="Light Piece" />
                }
                break;
              }
            }
          }
          /* If this is a piece, it is a current human player turn, the piece belongs to the
          current player, and piece can move*/
          let pieces_turn = props.game.pieces_turn ? 0 : 1
          if (cellContent && !props.game.ai_players[0][pieces_turn] &&
            cellContent.color === props.game.pieces_turn) {
            // Additional condition => if the piece belongs to possible moves set
            for (const key in props.game.game_state[2]) {
              if (parseInt(key) === cellContent.id) {
                // If firstMove => onClick always highlight a square,
                // otherways only jumping moves of the same piece are valid
                if (firstMove) cellClick = () => setSquaresToHighlight({[key]: props.game.game_state[2][key]})
              }
            }
          }
          // onClick on everything that is not selected pieces means clearing the board from highlighted squares
          if (!cellClick) cellClick = () => setSquaresToHighlight([])
        }
        row.push(
          <td key={j} className={cellClass} value={cellContent} onClick={cellClick}>
            {cellImage}
          </td>
        );
      }
      board.push(<tr key={i}>{row}</tr>)
    }
    // Highlight squares if squaresToHighlight exists
    if (squaresToHighlight) {
      for (const piece in squaresToHighlight) {
        for (const move of squaresToHighlight[piece]) {
          const updatedCell = React.cloneElement(board[move[0][0]].props.children[move[0][1]], {
            className: 'func-square highlighted-square',
            onClick: () => makeMove(piece, [move[0][0], move[0][1]], move[1]),
          })
          board[move[0][0]].props.children[move[0][1]] = updatedCell
        }
      }
    }
    return [...board]
  }

  const [squaresToHighlight, setSquaresToHighlight] = useState([])
  const [table, setTable] = useState([])
  const [firstMove, setFirstMove] = useState(true)

  useEffect(() => {
    setTable(generateTable())
  }, [squaresToHighlight])

  return (
    <div id="game-container">
      {/* <div>{JSON.stringify(props.game)}</div> */}
      <table>
        <tbody>{table}</tbody>
      </table>
    </div>
  )
}

export default CheckersContainer