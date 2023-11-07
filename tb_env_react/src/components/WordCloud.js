import React, {useEffect, useState} from "react";
import "./styling/WordCloud.css"
import ReactWordcloud from 'react-wordcloud';
import 'tippy.js/dist/tippy.css';





const WordCloud = ({cloud_type, County, timeFrame, AccountType}) => {

    const [words, setWords] = useState([]);
    const [rendered, setRendered] = useState(false)

    const fetchTerms = () => {
        fetch('http://127.0.0.1:5000/get_terms',
            {
                'method':'POST',
                headers : {
                    'Content-Type':'application/json'
                },
                body: JSON.stringify([cloud_type, timeFrame, County])
            })
            .then((response) => response.json())
            .then((data) => {
                setWords(data);
                console.log(words)
                setRendered(true)
            })
            .catch((error) => {
                console.error(error);
            });
    };

    useEffect(() => {
        fetchTerms()
    }, [rendered, cloud_type, County, timeFrame, AccountType]);

    const options = {
        rotations: 1,
        rotationAngles: [0],
        fontSizes: [15,60],

        colors: ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"],
        enableTooltip: true,
        deterministic: false,
        fontFamily: "impact",
        fontStyle: "normal",
        fontWeight: "normal",
        padding: 1,
        scale: "sqrt",
        spiral: "archimedean",
        transitionDuration: 1000

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

