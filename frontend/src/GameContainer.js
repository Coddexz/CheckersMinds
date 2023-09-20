import React, { useState } from 'react'
import PlayerForm from './PlayerForm'
import AIForm from './AIForm'


const GameContainer = () => {
    const [AIFirstVisible, setAIFirstVisible] = useState(false)
    const [AISecondVisible, setAISecondVisible] = useState(false)

    return (
        <div id="game-container">
            <div>
                Game rules:
            </div>
            <br />
            <div>
                <PlayerForm
                setAIFirstVisible={setAIFirstVisible}
                setAISecondVisible={setAISecondVisible}
                />
            </div>
            <div>
                {AIFirstVisible && <AIForm name='AI first player'/>}
            </div>
            <div>
                {AISecondVisible && <AIForm name='AI second player'/>}
            </div>
        </div>
    )
}

export default GameContainer