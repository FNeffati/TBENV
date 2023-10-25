import React, {useEffect, useState} from "react";
import TagCloud from "TagCloud"
import "./styling/WordCloud.css"




const WordCloud = () => {

    const [words, setWords] = useState([]);
    const fetchTerms = () => {
        fetch("http://127.0.0.1:5000/get_terms")
            .then((response) => response.json())
            .then((data) => {
                setWords(data);
            })
            .catch((error) => {
                console.error(error);
            });
    };

    useEffect(() => {
        fetchTerms()
    }, []);


    useEffect(() => {
        return () => {
                const container = ".tagcloud";
                const texts = words.map((word) => word.word);
                const options = {radius: 300, maxSpeed: "slow", keep: true};
                TagCloud(container, texts, options);
        }
    }, [words]);





    return (

        <div className="all">
            <div className="tagcloud"></div>
        </div>
    )
};

export default WordCloud