import React, { Component } from "react";
import { MapContainer, GeoJSON } from "react-leaflet";
import aoi from "./../data/Vector/AOI.json";
import cellt_1 from "./../data/Vector/cellt_1.json";
import "leaflet/dist/leaflet.css";
import "./TempMap.css";

async function logJSONData() {
    const response = await fetch("http://example.com/movies.json");
    const jsonData = await response.json();
    console.log(jsonData);
  }

class TempMap extends Component {
    state = {};
    render() {
        return (
            <div>
                <h1>Temp Map</h1>
                    <GeoJSON data={ aoi } />
                    <GeoJSON data={ cellt_1 } />
            </div>
        );
    }
}

export default TempMap;