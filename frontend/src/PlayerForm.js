import React from "react";


const PlayerForm = (props) => {

    const handleRadioChange = (event) => {
        const value = event.target.value
        switch (value) {
            case 'AI vs AI':
                props.setAIFirstVisible(true)
                props.setAISecondVisible(true)
                break

            case 'Human vs AI':
                props.setAIFirstVisible(false)
                props.setAISecondVisible(true)
                break

            case 'AI vs Human':
                props.setAIFirstVisible(true)
                props.setAISecondVisible(false)
                break

            default:
                props.setAIFirstVisible(false)
                props.setAISecondVisible(false)
        }
    }

    return (
        <div>
            <div>Please, select the type of players</div>
            <label>
                <input type='radio' value="AI vs AI" name="Players" onClick={handleRadioChange}/>
                AI vs AI
            </label>
            &nbsp; &nbsp; &nbsp;
            <label>
                <input type="radio" value="AI vs Human" name="Players" onClick={handleRadioChange}/>
                AI vs Human
            </label>
            &nbsp; &nbsp; &nbsp;
            <label>
                <input type="radio" value="Human vs AI" name="Players" onClick={handleRadioChange}/>
                Human vs AI
            </label>
            &nbsp; &nbsp; &nbsp;
            <label>
                <input type="radio" value="Human vs Human" name="Players" onClick={handleRadioChange}/>
                Human vs Human
            </label>
        </div>
    )
}

export default PlayerForm