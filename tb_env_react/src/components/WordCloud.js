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

    return (

        <div className="all">
            <ReactWordcloud
                words={words}
            />
        </div>
    )
};

export default WordCloud

