import React, {useEffect, useState} from "react";
import "./styling/WordCloud.css"
import ReactWordcloud from 'react-wordcloud';




const WordCloud = (cloud_type) => {

    const [words, setWords] = useState([]);
    const [rendered, setRendered] = useState(false)

    const fetchTerms = () => {
        fetch('http://127.0.0.1:5000/get_terms',
            {
                'method':'POST',
                headers : {
                    'Content-Type':'application/json'
                },
                body: JSON.stringify([cloud_type.cloud_type])
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
    }, [rendered, cloud_type.cloud_type]);

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

