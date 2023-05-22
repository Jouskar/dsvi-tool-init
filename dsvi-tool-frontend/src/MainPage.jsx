import './MainPage.css';
import TempMap from "./components/TempMap"
import reportWebVitals from './reportWebVitals';
import SelectionPanel from './components/SelectionPanel/SelectionPanel';
import { Map, MapContainer, TileLayer, Marker, Popup, GeoJSON } from 'react-leaflet';
//import vectors from "./vectors";
import React, { useState, useRef, useEffect } from "react";
import Form from "react-bootstrap/Form";
import useHttp, { endpoints } from './hooks/use-http';
import { ExpandMore } from '@mui/icons-material';
import {
  FormControlLabel, FormControl, FormLabel,
  RadioGroup, Radio,
  Drawer,
  List, ListItem,
  Typography,
  Divider,
  Accordion, AccordionSummary, AccordionDetails,
 } from '@mui/material';

const bbox = require('geojson-bbox');

//const extent = bbox(vectors.aoi);

const drawerWidth = 250;

function MainPage() {
  let geo;
  const [adminLevel, setAdminLevel] = useState("1");
  const [geoData, setGeoData] = useState(null);
  const [vectorDataList, setVectorDataList] = useState(null);
  const [vectorLayerList, setVectorLayerList] = useState(null);
  const [vectorLayer, setVectorLayer] = useState("cellt");
  const [country, setCountry] = useState("Tajikistan");

  const geoJsonRef = useRef(null);

  const parseVectorData = (data) => {
    setVectorDataList(data);
    setGeoData(JSON.parse(data[parseInt(adminLevel)-1].data_geojson));
  }

  const parseLayerTypes = (data) => {
    console.log(data)
    setVectorLayerList(data);
  }

  let requestConfigCountry = {
    method: 'GET',
    endpoint: endpoints.vector,
    query: {
      country: country,
      layer: vectorLayer,
    }
  }

  let requestConfigLayerTypes = {
    method: 'GET',
    endpoint: endpoints.layerTypes,
  }

  const {isLoading: isLayerLoading, error: errorLayer, sendRequest: fetchCountry} = useHttp(requestConfigCountry, parseVectorData);
  const {isLoading: isLayerTypeLoading, error: errorLayerType, sendRequest: fetchLayerTypes} = useHttp(requestConfigLayerTypes, parseLayerTypes);

  useEffect(() => {
    fetchLayerTypes();
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

  const changeSocioeconomicLayer = (event) => {
    if (event.target.checked) {
      const selectedSocioeconomicLayer = event.target.value;
      setVectorLayer(selectedSocioeconomicLayer);
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
          <Accordion>
            <AccordionSummary
              expandIcon={<ExpandMore />}
              aria-controls="socioeconomic-layers"
              id="socioeconomic-layers-header"
            >
              <Typography>Socioeconomic Layers</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <FormControl>
                <RadioGroup
                  aria-labelledby="socioeconomic-layers-label"
                  name="socioeconomic-layers-group"
                  value={vectorLayer}
                  onChange={changeSocioeconomicLayer}
                >
                  {vectorLayerList?.map((layer, index) => (
                    <FormControlLabel sx={{
                      '& .MuiSvgIcon-root': {
                      fontSize: 15,
                      },
                      '& .MuiTypography-root': {
                      fontSize: 15,
                      },
                    }} key={layer.name} value={layer.name} control={<Radio />} label={layer.description} />
                  ))}
                </RadioGroup>
              </FormControl>
            </AccordionDetails>
          </Accordion>
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
