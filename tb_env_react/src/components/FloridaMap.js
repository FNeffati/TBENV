import React from 'react';
import { MapContainer, TileLayer, GeoJSON } from 'react-leaflet';
import floridaCounties from './geojson-fl-counties-fips.json';
import "./styling/FloridaMap.css"

const FloridaMap = () => {
    return (
        <div className="map_div">
            <MapContainer center={[27.766279, -88]} zoom={6} style={{height: 600, width:'100%'}}>
                <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
                <GeoJSON data={floridaCounties} />
            </MapContainer>

        </div>
    )
}
export default FloridaMap;