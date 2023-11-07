import React, { useState, useEffect } from 'react';
import "./styling/Twitter.css"
import WordCloud from "./WordCloud";

function Twitter({timeFrame, County, AccountType, WordCloudOption}) {
    const [tweets, setTweets] = useState([]);

    const fetchTweets = () => {
        fetch('http://127.0.0.1:5000/get_tweets',
            {
                'method':'POST',
                headers : {
                    'Content-Type':'application/json'
                },
                body: JSON.stringify([timeFrame, County, AccountType])
            })
            .then((response) => response.json())
            .then((data) =>(
                setTweets(data))
            )
            .catch((error) => console.error(error));
    };

    useEffect(() => {
        fetchTweets();
    }, [timeFrame, County, AccountType]);

    const [searchTerm, setSearchTerm] = useState('');

    const highlightText = (text, term) => {
        const regex = new RegExp(term, 'gi');
        return text.replace(regex, (match) => `<span class="highlight">${match}</span>`);
    };

    const filteredTweets = tweets.filter((tweet) =>
        tweet.text.toLowerCase().includes(searchTerm.toLowerCase())

    );

return (
        <div className="Twitter_Section">

                <div className="tweets_header">
                    <button className="tweet_refresher" onClick={fetchTweets}>Refresh</button>
                    <input
                        className="tweet_search_bar"
                        type="text"
                        placeholder="Filter tweets"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
            </div>

            <div className="mid">
                <div className="tweets_container">
                    <ul>
                        {Array.isArray(filteredTweets) && filteredTweets.length > 0 ? (
                            filteredTweets.map((tweet) => (
                                <div className="tweet">

                                    <div className="tweet_top">
                                        <img
                                            src={tweet.image}
                                            alt={"#"}
                                            className="profile_image"
                                        />
                                        <a className="username" href={"http://www.x.com/" + tweet.username}>@{tweet.username}</a>
                                    </div>

                                    <div className="tweet_mid">
                                        <p
                                            className="tweet_text"
                                            dangerouslySetInnerHTML={{
                                                __html: highlightText(tweet.text, searchTerm),
                                            }}
                                        ></p>
                                    </div>

                                    <div className="tweet_bottom">
                                        <p className="tweet_time">{tweet.time}</p>
                                        <p className="tweet_location">{tweet.location}</p>
                                    </div>

                                </div>
                            ))
                        ) : (
                            <div className="tweet_mid">

                                <p className="no_match">No Tweets match your filters.</p>
                            </div>
                        )}
                    </ul>
                </div>

            </div>

        </div>
    );
}

export default Twitter;
