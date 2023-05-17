import React, { Component } from "react";
import { MapContainer, GeoJSON } from "react-leaflet";
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
            </div>
        );
    }
}

export default TempMap;