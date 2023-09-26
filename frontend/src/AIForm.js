import React from "react";


const AIForm = (props) => {

    const handleRadioChange = (event) => {
        const value = event.target.value
        if (props.name === 'AI first player') {
            props.setGameInitData((prevState) => ({
                ...prevState,
                AIFirst: value,
            }))
        } else {
            props.setGameInitData((prevState) => ({
                ...prevState,
                AISecond: value,
        }))
    }}

    return (
        <div>
            <br></br>
            <div>Please, select the type of the {props.name}</div>
            <label>
                <input type='radio' value="random" name={props.name} onClick={handleRadioChange} />
                random
            </label>
            &nbsp; &nbsp; &nbsp;
            <label>
                <input type="radio" value="minimax" name={props.name} onClick={handleRadioChange} />
                minimax
            </label>
            &nbsp; &nbsp; &nbsp;
            <label>
                <input type="radio" value="deep q-learning" name={props.name} onClick={handleRadioChange} />
                deep q-learning
            </label>
        </div>
    )
}

export default AIForm