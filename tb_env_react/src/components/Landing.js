import React, {useEffect, useState} from 'react';
import './styling/landing.css'
import Header from "./Header";
import Twitter from "./Twitter";
import WordCloud from "./WordCloud";
import FloridaMap from "./FloridaMap";
import DropDown from "./DropDown";



function Landing () {

    const [County_Options, setCountyOptions] = useState([])
    useEffect(() => {
        fetch('http://localhost:5000/get_counties')
            .then(response => response.json())
            .then(data => setCountyOptions(data))
            .catch(error => console.error(error));
    }, []);

    const Time_Frame_Options = ["1 Day", "1 Week", "1 Month", "1 Year", "Custom"]
    const Word_Cloud_Options = ["Geo Tags", "Non-Geo Tags"]

    const [SelectedTimeFrame, setTimeFrame] = useState("")
    const [SelectedWordCloudOption, setWordCloudOption] = useState("")
    const [SelectedCountyOption, setCountyOption] = useState("")
    const callback = (value, context) => {
        switch (context) {
            case "TimeFrame":
                setTimeFrame(value)
                console.log("Time Frame selected:", value);
                break;
            case "WordCloudOption":
                setWordCloudOption(value)
                console.log("Word Cloud Option selected:", value);
                break;
            case "CountyOption":
                setCountyOption(value)
                console.log("County Option selected:", value);
                break;
            default:
                break;
        }
    };




        return (
        <div>
            <Header/>
            <div className="dropDowns">
                <DropDown
                    callback={(value) => callback(value, "TimeFrame")}
                    title="Select Time Frame"
                    options={Time_Frame_Options}
                />
                <DropDown
                    callback={(value) => callback(value, "WordCloudOption")}
                    title="Select Word Cloud Focus"
                    options={Word_Cloud_Options}
                />
                <DropDown
                    callback={(value) => callback(value, "CountyOption")}
                    title="Select County"
                    options={County_Options}
                />

            </div>
            <div className="landing_container">
                <div className="left_side">
                     <Twitter timeFrame={SelectedTimeFrame} County={SelectedCountyOption}/>
                </div>

                <div className="middle_side">

                    <div className="word_cloud_container">
                        <WordCloud cloud_type={SelectedWordCloudOption} />
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