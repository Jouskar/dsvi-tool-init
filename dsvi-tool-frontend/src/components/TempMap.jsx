import React, { Component } from "react";
import { MapContainer, GeoJSON } from "react-leaflet";
import aoi from "./../data/Vector/AOI.json";
import "leaflet/dist/leaflet.css";
import "./TempMap.css";

class TempMap extends Component {
    state = {};

    render() {
        return (
            <div>
                <h1>Temp Map</h1>
                <MapContainer style={{ height: "80vh" }} zoom={7} center={[39, 70]}>
                    <GeoJSON data={ aoi } />
                </MapContainer>
            </div>
        );
    }
}

export default TempMap;