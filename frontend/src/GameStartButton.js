import React, { useEffect, useState } from "react"


const GameStartButton = (props) => {

    const [buttonDisabled, setButtonDisabled] = useState(true)

    const convertPlayers = (playersToConvert) => {
        switch (playersToConvert) {
            case 'AI vs AI':
                return ([true, true])

            case 'Human vs AI':
                return ([false, true])

            case 'AI vs Human':
                return ([true, false])

            case 'Human vs Human':
                return ([false, false])

            default:
                return ([null, null])
        }
    }

    useEffect(() => {
        if (props.gameInitData.players !== null) {
            switch (props.gameInitData.players) {

                case 'AI vs AI':
                    if (props.gameInitData.AIFirst !== null &&
                        props.gameInitData.AISecond !== null) {
                            setButtonDisabled(false)
                        } else {
                            setButtonDisabled(true)
                        }
                    break

                case 'Human vs AI':
                    if (props.gameInitData.AISecond !== null) {
                        setButtonDisabled(false)
                    } else {
                        setButtonDisabled(true)
                    }
                    break

                case 'AI vs Human':
                    if (props.gameInitData.AIFirst !== null) {
                        setButtonDisabled(false)
                    } else (setButtonDisabled(true))
                    break

                default:
                    setButtonDisabled(false)
            }
        } else {
            setButtonDisabled(true)
        }
    }, [props.gameInitData])

    const handleClick = () => {
        // Make a fetch request to the `/game/init` endpoint.
        // const data = JSON.stringify({...props.gameInitData, players: convertPlayers(props.gameInitData.players)})

        fetch("http://127.0.0.1:5000/game/init", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                ...props.gameInitData,
                players: convertPlayers(props.gameInitData.players)
            })
        })
        .then((res) => {
            if (!res.ok) {
                throw new Error('Network response was not ok');
            }
            return res.json();
        })
        .then((checkersGame) => {
            // Set the checkersGame state with the JSON response.
            props.setGame(checkersGame);
        })
        .catch((err) => {
            // Handle errors and show a user-friendly message.
            console.error('Error:', err);
            alert('An error occurred while fetching the game data.');
        });
    }
    
      

    return (
        <div>
            <br></br>
            <button onClick={handleClick} disabled={buttonDisabled} id="game-start-button">
                Start
            </button>
        </div>
    )
}

export default GameStartButton