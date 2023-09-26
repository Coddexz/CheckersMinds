import React, { useState } from 'react'
import PlayerForm from './PlayerForm'
import AIForm from './AIForm'
import GameStartButton from './GameStartButton'
import ShowRulesButton from './ShowRulesButton'


const GameContainer = (props) => {
    const [AIFirstVisible, setAIFirstVisible] = useState(false)
    const [AISecondVisible, setAISecondVisible] = useState(false)

    const [gameInitData, setGameInitData] = useState({
        players: null,
        AIFirst: null,
        AISecond: null,
    })

    return (
        <div id="game-container">
            <div>
                Game rules: <ShowRulesButton setShowRules={props.setShowRules}/>
            </div>
            <br />
            <div>
                <PlayerForm
                setAIFirstVisible={setAIFirstVisible}
                setAISecondVisible={setAISecondVisible}
                setGameInitData={setGameInitData}
                />
            </div>
            <div>
                {AIFirstVisible && <AIForm
                name='AI first player'
                setGameInitData={setGameInitData}
                />}
            </div>
            <div>
                {AISecondVisible && <AIForm
                name='AI second player'
                setGameInitData={setGameInitData}
                />}
            </div>
            <div>
                <GameStartButton
                gameInitData={gameInitData}
                />
            </div>
        </div>
    )
}

export default GameContainer