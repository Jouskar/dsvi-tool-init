import './MainPage.css';
import TempMap from "./components/TempMap"
import reportWebVitals from './reportWebVitals';
import SelectionPanel from './components/SelectionPanel/SelectionPanel';
import { Map, MapContainer, TileLayer, Marker, Popup, GeoJSON } from 'react-leaflet';
//import vectors from "./vectors";
import React, { useState, useRef, useEffect } from "react";
import Form from "react-bootstrap/Form";
import useHttp, { endpoints } from './hooks/use-http';

import {
  FormControlLabel,
  FormControl,
  FormLabel,
  RadioGroup, 
  Radio,
  Drawer,
  List,
  ListItem,
  Typography,
  Divider,

 } from '@mui/material';

const bbox = require('geojson-bbox');

//const extent = bbox(vectors.aoi);

const drawerWidth = 250;

function MainPage() {
  let geo;
  const [adminLevel, setAdminLevel] = useState(1);
  const [geoData, setGeoData] = useState(null);
  const [vectorDataList, setVectorDataList] = useState(null);
  const [vectorLayerList, setVectorLayerList] = useState(null);
  const [vectorLayer, setVectorLayer] = useState("cellt");
  const [country, setCountry] = useState("Tajikistan");

  const geoJsonRef = useRef(null);

  const parseVectorData = (data) => {
    setVectorLayerList(data);
  }

  const parseLayerTypes = (data) => {
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

  const {isLayerLoading, errorLayer, sendRequest: fetchCountry} = useHttp(requestConfig, parseVectorData);
  const {isLayerTypeLoading, errorLayerType, sendRequest: fetchLayerTypes} = useHttp(requestConfig, parseVectorData);

  useEffect(() => {

  }, []);

  useEffect(() => {
    fetchCountry();
  }, [vectorLayer]);
  
  useEffect(() => {
    console.log(adminLevel-1);
    if (geoJsonRef.current) {
      geoJsonRef.current.clearLayers().addData(geoData);
    }
  }, [geoData]);

  const changeAdminLevel = (event) => {

    if (event.target.checked) {
      const selectedAdminLevel = parseInt(event.target.value);
      setAdminLevel(selectedAdminLevel);
      setGeoData(JSON.parse(vectorDataList[selectedAdminLevel-1].data_geojson));
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
      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: drawerWidth,
            boxSizing: 'border-box',
          },
        }}
      >
        <List>
          <ListItem>
            <Typography>MAIN MENU</Typography>
          </ListItem>
          <Divider/>
          <ListItem>
            <FormControl>
              <FormLabel id="admin-level-label">Select administrative level</FormLabel>
              <RadioGroup
                row
                aria-labelledby="admin-level-label"
                name="admin-level-group"
                value={adminLevel}
                onChange={changeAdminLevel}
              >
                {["One", "Two", "Three"].map((text, index) => (
                  <FormControlLabel sx={{
                    '& .MuiSvgIcon-root': {
                    fontSize: 15,
                    },
                    '& .MuiTypography-root': {
                    fontSize: 15,
                    },
                  }} key={text} value={index+1} control={<Radio />} label={text} />
                ))}
              </RadioGroup>
            </FormControl>
          </ListItem>
          <Divider/>
          <ListItem>
          </ListItem>
          <ListItem>
          </ListItem>
        </List>
      </Drawer>
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
