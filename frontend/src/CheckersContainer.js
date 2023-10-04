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

    for (const piece of props.game.pieces_dark) {
      if (piece[0] === pieceToMoveId) {
        pieceToMove = {'id': piece[0], 'color': piece[1], 'position': piece[2], 'king': piece[3]}
        break
      }
    }
    if (!pieceToMove) {
      for (const piece of props.game.pieces_light) {
        if (piece[0] === pieceToMoveId) {
          pieceToMove = {'id': piece[0], 'color': piece[1], 'position': piece[2], 'king': piece[3]}
          break
        }
      }
    }
    console.log('Piece to move')
    console.log(pieceToMove)
    console.log('highlighted pos')
    console.log(highlightedPosition)
    setFirstMove(false)
    let boardToUpdate = undefined
    let highlightedPositionStr = highlightedPosition[0].toString() + highlightedPosition[1]

    // Change the board object
    let boardObject = [...props.game.board]
    boardObject[parseInt(highlightedPositionStr)] = pieceToMove.id
    boardObject[parseInt(pieceToMove.position[0].toString() + pieceToMove.position[1])] = null

    // Change pieces counter and array
    let piecesArr = pieceToMove.color ? [...props.game.pieces_dark] : [...props.game.pieces_light]
    // To be continued, it doesn't change the value of piece in the array!!!
    for (const [i, piece] of piecesArr.entries()) {
      if (piece[0] === pieceToMove.id) {
        piecesArr[i][2] = [highlightedPosition[0], highlightedPosition[1]]
      }
    }

    if (jump) {
      let newPiecesCounter = props.game.pieces_counter - 1

      // Check the enemy position
      const heightEqualizer = (highlightedPosition[0] - pieceToMove.position[0]) > 0 ? 1 : -1
      const widthEqualizer = (highlightedPosition[1] - pieceToMove.position[1]) > 0 ? 1 : -1

      let enemyPieceHeight = pieceToMove.position[0]
      let enemyPieceWidth = pieceToMove.position[1]
      const enemyPieceModifier = pieceToMove.color ? 2 : 1
      const minEnemyPieceId = pieceToMove.color ? 20 : 0
      const maxEnemyPieceId = (((props.game.height - 2) / 2) * (props.game.width / 2)) * enemyPieceModifier
      
      
      while (true) {
        enemyPieceHeight += heightEqualizer
        enemyPieceWidth += widthEqualizer
        const boardObjectSquare = boardObject[parseInt(enemyPieceHeight.toString() + enemyPieceWidth)]
        if (boardObjectSquare != null && minEnemyPieceId <= boardObjectSquare && boardObjectSquare < maxEnemyPieceId) break
      }
      console.log('enemy piece position')
      console.log(enemyPieceHeight)
      console.log(enemyPieceWidth)
      let enemyPiecePosStr = enemyPieceHeight.toString() + enemyPieceWidth
      console.log('enemy piece to str')
      console.log(enemyPiecePosStr)
      boardObject[parseInt(enemyPiecePosStr)] = null

      let enemyPiecesArr = pieceToMove.color ? [...props.game.pieces_light] : [...props.game.pieces_dark]
      for (let i = 0; i < enemyPiecesArr.length; i++) {
        if (enemyPiecesArr[i][2][0] === enemyPieceHeight && enemyPiecesArr[i][2][1] === enemyPieceWidth) {
          console.log('enemy piece spotted')
          enemyPiecesArr.splice(i, 1)
        }}
      boardToUpdate = {
        'board': boardObject,
        'pieces_counter': newPiecesCounter,
        [pieceToMove.color ? 'pieces_dark' : 'pieces_light']: piecesArr,
        [pieceToMove.color ? 'pieces_light' : 'pieces_dark']: enemyPiecesArr,
      }
      } else {
        boardToUpdate = {
          'board': boardObject,
          [pieceToMove.color? 'pieces_dark' : 'pieces_light']: piecesArr,
        }
      }

    // If the piece crossed reached the end of the board => make it a king
    if ((pieceToMove.color && highlightedPosition[0] === (props.game.height - 1)) ||
    (!pieceToMove.color && highlightedPosition[0] === 0)) {
      for (const [i, piece] of piecesArr.entries()) {
        if (piece[0] === pieceToMove.id) {
          piecesArr[i][3] = true
        }
      }
      boardToUpdate = {...boardToUpdate, [pieceToMove.color ? 'pieces_dark' : 'pieces_light']: piecesArr,}
    }
    // Save the game state
    const {game_state, ...gameWithoutGameState} = props.game
    const updatedGameWithoutGameState = {...gameWithoutGameState, ...boardToUpdate}
    props.setGame({...props.game, ...boardToUpdate})

    // If this piece can make any other moves -> highlight position and allow for making only them
    if (jump) {
      for (const piece in squaresToHighlight) {
        if (parseInt(piece) === pieceToMove.id) {
          let possibleNextMoves = []
          for (const move of squaresToHighlight[piece]) {
            // console.log(move)
            // console.log(highlightedPosition)
            if (move[0][0][0] === highlightedPosition[0] && move[0][0][1] === highlightedPosition[1]) {
              const moveToBeAdded = [move[0].slice(1), move[1]]
              // console.log('Move to be added:')
              // console.log(moveToBeAdded)
              if (moveToBeAdded[0].length !== 0) possibleNextMoves.push(moveToBeAdded)
            }
          }
          console.log(possibleNextMoves)
          if (possibleNextMoves.length !== 0) {
            setSquaresToHighlight({[piece]: possibleNextMoves})
            return
          }
        }
      }
    }
    sendGame(updatedGameWithoutGameState)
    setSquaresToHighlight(null)
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
      // setSquaresToHighlight([])
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
                if (firstMove) {
                  cellClick = () => setSquaresToHighlight({[key]: props.game.game_state[2][key]})
                }
              }
            }
          }
          // onClick on everything that is not selected pieces means clearing the board from highlighted squares
          if (!cellClick && firstMove) cellClick = () => setSquaresToHighlight([])
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
          if (move[1]) {
            // If jump
            const updatedCell = React.cloneElement(board[move[0][0][0]].props.children[move[0][0][1]],
              {className: 'func-square highlighted-square',
              onClick: () => makeMove(parseInt(piece), [move[0][0][0], move[0][0][1]], move[1]),})
            board[move[0][0][0]].props.children[move[0][0][1]] = updatedCell
          } else {
            const updatedCell = React.cloneElement(board[move[0][0]].props.children[move[0][1]],
              {className: 'func-square highlighted-square',
              onClick: () => makeMove(parseInt(piece), [move[0][0], move[0][1]], move[1]),})
              board[move[0][0]].props.children[move[0][1]] = updatedCell
            }
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
  }, [squaresToHighlight, props.game])

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