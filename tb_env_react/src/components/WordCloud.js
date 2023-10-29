import React, {useEffect, useState} from "react";
import "./styling/WordCloud.css"
import ReactWordcloud from 'react-wordcloud';




const WordCloud = () => {

    const [words, setWords] = useState([]);
    const [rendered, setRendered] = useState(false)

    const fetchTerms = () => {
        fetch("http://127.0.0.1:5000/get_terms")
            .then((response) => response.json())
            .then((data) => {
                setWords(data);
                setRendered(true)
            })
            .catch((error) => {
                console.error(error);
            });
    };

    useEffect(() => {
        fetchTerms()
    }, [rendered]);

    const options = {
        rotations: 1,
        rotationAngles: [0],
        fontSizes: [15,70]
    };
    const size = [500, 600];

    return (

        <div className="all">
            <ReactWordcloud
                words={words}
                options={options}
                size={size}
                padding={0}

            />
        </div>
    )
};

export default WordCloud

