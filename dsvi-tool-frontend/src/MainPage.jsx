import './MainPage.css';
import TempMap from "./components/TempMap"
import reportWebVitals from './reportWebVitals';
import SelectionPanel from './components/SelectionPanel/SelectionPanel';
import { Map, MapContainer, TileLayer, Marker, Popup, GeoJSON } from 'react-leaflet';
//import vectors from "./vectors";
import React, { useState, useRef, useEffect } from "react";
import Form from "react-bootstrap/Form";
import useHttp, { endpoints } from './hooks/use-http';

const bbox = require('geojson-bbox');

//const extent = bbox(vectors.aoi);

function MainPage() {
  let geo;
  const [adminLevel, setAdminLevel] = useState(1);
  const [geoData, setGeoData] = useState(null);
  const [vectorDataList, setVectorDataList] = useState(null);
  const [vectorLayer, setVectorLayer] = useState("cellt");
  const [country, setCountry] = useState("Tajikistan");

  const geoJsonRef = useRef(null);

  const parseVectorData = (data) => {
    setVectorDataList(data);
    setGeoData(JSON.parse(data[0].data_geojson));
  }

  let requestConfig = {
    method: 'GET',
    endpoint: endpoints.vector,
    query: {
      country: country,
      layer: vectorLayer,
    }
  }

  const {isLoading, error, sendRequest: fetchCountry} = useHttp(requestConfig, parseVectorData);

  useEffect(() => {
    fetchCountry();
  }, []);
  
  useEffect(() => {
    console.log(geoData);
    console.log(adminLevel-1);
    if (geoJsonRef.current) {
      geoJsonRef.current.clearLayers().addData(geoData);
    }
  }, [adminLevel, geoData]);

  const changeAdminLevel = (event) => {

    if (event.target.checked) {
      setAdminLevel(event.target.value);
      //setGeoData(vectors.ndvi[adminLevel-1]);
      console.log(geoData);
    }
  }


  const onEachRegion = (region, layer) => {
    layer.bindPopup(
      `${region.properties.NAME_1}/${region.properties.NAME_2} 
    count: ${region.properties._count}
    sum: ${region.properties._sum}
    `)
  }
  return (
    <div className='flex-container'>
      <div className="sidebar">
        <h3 className="text-center mt-2">MAIN MENU</h3>
        <hr className="mt-2 mb-3" />

        <div className="container">
          <div className="row">
            <div className="col-sm-12">
              Select administrative level
            </div>
          </div>
          <div className="row mt-2">
            <Form>
              <div key={"admin-level-div"} className="mb-3">
                <Form.Check
                  inline
                  value="1"
                  label="One"
                  name="admin-level"
                  type={'radio'}
                  id={"admin-level-1"}
                  defaultChecked={true}
                  onChange={changeAdminLevel}
                />
                <Form.Check
                  inline
                  value="2"
                  label="Two"
                  name="admin-level"
                  type={'radio'}
                  id={"admin-level-2"}
                  onChange={changeAdminLevel}
                />
                <Form.Check
                  inline
                  value="3"
                  label="Three"
                  name="admin-level"
                  type={'radio'}
                  id={"admin-level-3"}
                  onChange={changeAdminLevel}
                />
              </div>
            </Form>
          </div>
        </div>
      </div>
      <MapContainer center={[39, 70]} zoom={9} scrollWheelZoom={true}
        whenReady={e => {
          //e.target.flyToBounds([
            //[extent[1], extent[0]],
            //</div>[extent[3], extent[2]]

          //]);
        }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <GeoJSON
          ref={geoJsonRef}
          data={geoData}
          onEachFeature={onEachRegion}
        />
      </MapContainer>
    </div>

  );
}

export default MainPage;
