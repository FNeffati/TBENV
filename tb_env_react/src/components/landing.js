import React from 'react';
import './styling/landing.css'
import Header from "./Header";
import Twitter from "./Twitter";
import WordCloud from "./WordCloud";
import FloridaMap from "./FloridaMap";



function Landing () {


    return (
        <div>
            <Header/>
            <div className="landing_container">
                <div className="left_side">
                     <Twitter/>
                </div>

                <div className="middle_side">

                    <div className="word_cloud_container">
                        <WordCloud />
                    </div>

                </div>

                <div className="right_side">
                    <FloridaMap/>
                </div>
            </div>
        </div>
    );

}

export default Landing;