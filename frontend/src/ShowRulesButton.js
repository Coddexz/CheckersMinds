import React from "react"


const ShowRulesButton = (props) => {

    const handleClick = () => {
        props.setShowRules(true)
    }
    return (
        <>
            &nbsp; &nbsp;
            <button type="button" onClick={handleClick} id="rules-button">
                Click me
            </button>
        </>
    )
}

export default ShowRulesButton