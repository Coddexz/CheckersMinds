import React from "react";


const AIForm = (props) => {
    return (
        <div>
            <div>Please, select the type of the {props.name}</div>
            <label>
                <input type='radio' value="random" name={props.name} />
                random
            </label>
            &nbsp; &nbsp; &nbsp;
            <label>
                <input type="radio" value="minimax" name={props.name} />
                minimax
            </label>
            &nbsp; &nbsp; &nbsp;
            <label>
                <input type="radio" value="deep q-learning" name={props.name} />
                deep q-learning
            </label>
        </div>
    )
}

export default AIForm