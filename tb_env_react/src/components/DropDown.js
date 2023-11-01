import React, {useState} from "react"
import "./styling/DropDown.css"


const DropDown = ({callback, title, options}) => {

    const [selectedOption, setSelectedOption] = useState(null);
    const [showOptions, setShowOptions] = useState(false);

    const onSelect = (data) =>{
        callback(data)
    }
    const handleOptionSelect = (option) => {
        setSelectedOption(option);
        onSelect(option);
        setShowOptions(false);
    };


    return(
        <div className="dd_container">
            <div className="dropdown-header" onClick={() => setShowOptions(!showOptions)}>
                {selectedOption || title} {}
                <span className={`dropdown-arrow ${showOptions ? 'up' : 'down'}`}></span>
            </div>
            <div className="options_menu">
                {showOptions && (
                    <ul className="options">
                        {options.map((option) => (
                            <li className="single_option" key={option} onClick={() => handleOptionSelect(option)}>
                                {option}
                            </li>
                        ))}
                    </ul>
                )}
            </div>
        </div>
    )
}

export default DropDown;