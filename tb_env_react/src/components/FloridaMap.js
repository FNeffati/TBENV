import React, { useEffect } from 'react';
import { MapContainer, TileLayer, GeoJSON } from 'react-leaflet';
import floridaCounties from './geojson-fl-counties-fips.json';
import "./styling/FloridaMap.css"

const FloridaMap = ({ userSelectedCounty }) => {
    const [highlightedCounty, setHighlightedCounty] = React.useState(null);

    const style = (feature) => {
        if (feature.properties.NAME === userSelectedCounty) {
            return {
                fillColor: 'red',
                weight: 2,
                opacity: 1,
                color: 'white',
            };
        }
        return {
            fillColor: 'blue',
            weight: 2,
            opacity: 1,
            color: 'white',
        };
    };

    useEffect(() => {
        if (userSelectedCounty) {
            setHighlightedCounty(userSelectedCounty);
        } else {
            setHighlightedCounty(null);
        }
    }, [userSelectedCounty]);

    return (
        <div className="map_div">
            <MapContainer center={[27.766279, -86.798]} zoom={6} style={{ height: 600, width: '100%' }}>
                <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
                <GeoJSON data={floridaCounties} style={style} />
            </MapContainer>
        </div>
    );
};

export default FloridaMap;
