import React, { useState, useEffect } from 'react';
import "./styling/Twitter.css"
import WordCloud from "./WordCloud";

function Twitter() {
    const [tweets, setTweets] = useState([]);

    const fetchTweets = () => {
        fetch('http://127.0.0.1:5000/get_tweets')
            .then((response) => response.json())
            .then((data) =>(
                setTweets(data))

            )
            .catch((error) => console.error(error));
    };

    useEffect(() => {
        fetchTweets();
    }, []);

    const [searchTerm, setSearchTerm] = useState('');


    const filteredTweets = tweets.filter((tweet) =>
        tweet.text.toLowerCase().includes(searchTerm.toLowerCase())
    );

return (
        <div className="Twitter_Section">
            <div className="top">

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

                <div className="word_cloud_header">
                    <h1>Word Cloud</h1>
                </div>

            </div>

            <div className="mid">
                <div className="tweets_container">
                    <ul>
                        {Array.isArray(filteredTweets) && filteredTweets.length > 0 ? (
                            filteredTweets.map((tweet) => (
                                <div className="tweet">
                                    <div className="top">
                                        <img
                                            src={tweet.image ? tweet.image : './styling/avatar.png'}
                                            alt={"#"}
                                            className="profile_image"
                                        />

                                        <a className="username" href={"http://www.x.com/" + tweet.username}>@{tweet.username}</a>
                                    </div>
                                    <div className="tweet_mid">
                                        <p className="tweet_text">{tweet.text}</p>
                                    </div>
                                    <div className="tweet_bottom">
                                        <p className="tweet_time">{tweet.time}</p>
                                        <p className="tweet_location">{tweet.location}</p>
                                    </div>

                                </div>
                            ))
                        ) : (
                            <li>No tweets available.</li>
                        )}
                    </ul>
                </div>

                <div className="word_cloud_container">
                    <WordCloud />
                </div>

            </div>

        </div>
    );
}

export default Twitter;
