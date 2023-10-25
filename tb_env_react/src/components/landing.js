import React from 'react';
import './styling/landing.css'
import myImage from "./styling/tbaylanding.jpg"
import Header from "./Header";



function Landing () {


    return (
        <div>
            <Header/>
            <div className="landing_container">
                <div className="leftSide">
                    <h1>Tampa Bay Environmentalist</h1>

                    <div className="email_container">
                        <input type="email" className="email-input" placeholder="Join our news letter for the latest news."></input>
                            <button className="submit-button">Submit</button>
                    </div>

                </div>

                <div className="image-container">
                    <img className="tbayImage" src={myImage} alt="" />
                </div>
            </div>
        </div>
    );

}

export default Landing;