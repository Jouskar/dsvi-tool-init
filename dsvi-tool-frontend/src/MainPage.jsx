import "./MainPage.css";
import L from "leaflet";
import TempMap from "./components/TempMap";
import reportWebVitals from "./reportWebVitals";
import SelectionPanel from "./components/SelectionPanel/SelectionPanel";
import {
  Map,
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  GeoJSON,
  useMap,
} from "react-leaflet";
//import vectors from "./vectors";
import React, { useState, useRef, useEffect } from "react";
import useHttp, { endpoints } from "./hooks/use-http";
import {
  Typography,
  Modal,
  Box,
  IconButton,
  Grid,
  Button,
  FormGroup,
  FormControlLabel,
  Checkbox,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from "@mui/material";
import { PaidOutlined, TroubleshootOutlined } from "@mui/icons-material";

const bbox = require("geojson-bbox");

//const extent = bbox(vectors.aoi);

const style = {
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: 400,
  bgcolor: "background.paper",
  border: "2px solid #000",
  boxShadow: 24,
  p: 4,
};

function GeoJSONHandler(props) {
  const MAP = useMap();

  const onEachRegion = (region, layer) => {
    layer.bindPopup(
      `${region.properties.NAME_1}/${region.properties.NAME_2} 
    count: ${region.properties._count}
    sum: ${region.properties._sum}
    `
    );
    console.log(layer);
    if (layer.feature._max < parseInt(props.critiqueValue)) {
      layer.options.color = "red";
    }
  };

  const parseVectorData = (data) => {
    const geoJson = L.geoJSON(
      JSON.parse(data[parseInt(props.adminLevel) - 1].geojson_str)
    );
    props.setVectorDataList(data);
    props.setGeoJson(geoJson);
    props.setGeoData(
      JSON.parse(data[parseInt(props.adminLevel) - 1].geojson_str)
    );
    props.setCritiqueValue(
      JSON.parse(data[parseInt(props.adminLevel) - 1].critique_value)
    );

    MAP.fitBounds(geoJson.getBounds());
    MAP.setMaxBounds(geoJson.getBounds());
    MAP.options.minZoom = MAP.getBoundsZoom(geoJson.getBounds());
  };

  let requestConfigCountry = {
    method: "GET",
    endpoint: endpoints.vector,
    query: {
      country: props.country,
      layer: props.vectorLayer,
    },
  };

  const {
    isLoading: isLayerLoading,
    error: errorLayer,
    sendRequest: fetchCountry,
  } = useHttp(requestConfigCountry, parseVectorData);

  useEffect(() => {
    fetchCountry();
  }, [props.vectorLayer]);

  return (
    <GeoJSON
      ref={props.geoJsonRef}
      data={props.geoData}
      onEachFeature={onEachRegion}
    />
  );
}

function MainPage() {
  const [adminLevel, setAdminLevel] = useState("1");
  const [geoData, setGeoData] = useState(null);
  const [geoJson, setGeoJson] = useState(null);
  const [vectorDataList, setVectorDataList] = useState(null);
  const [vectorLayerList, setVectorLayerList] = useState(null);
  const [vectorLayer, setVectorLayer] = useState("cellt");
  const [country, setCountry] = useState("Tajikistan");
  const [critiqueValue, setCritiqueValue] = useState("0");
  const [vectorAnalyze, setVectorAnalyze] = useState([]);
  const [open, setOpen] = React.useState(false);
  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  const geoJsonRef = useRef(null);

  const addVectorAnalyze = (event) => {
    let temp = vectorAnalyze;

    if (event.target.checked) {
      temp.push(event.target.value);
      setVectorAnalyze(temp);
    } else {
      let index;
      for (let i = 0; i < vectorAnalyze.length; i++) {
        if (vectorAnalyze[i] === event.target.value) {
          index = i;
          break;
        }
      }
      temp.splice(index, 1);
      setVectorAnalyze(temp);
    }

    console.log(vectorAnalyze);
  };

  const handleVectorAnalyze = () => {};

  const parseLayerTypes = (data) => {
    console.log(data);
    setVectorLayerList(data);
  };

  let requestConfigLayerTypes = {
    method: "GET",
    endpoint: endpoints.layerTypes,
  };

  const {
    isLoading: isLayerTypeLoading,
    error: errorLayerType,
    sendRequest: fetchLayerTypes,
  } = useHttp(requestConfigLayerTypes, parseLayerTypes);

  useEffect(() => {
    fetchLayerTypes();
  }, []);

  useEffect(() => {
    console.log(adminLevel - 1);
    if (geoJsonRef.current) {
      geoJsonRef.current.clearLayers().addData(geoData);
    }
  }, [geoData]);

  const changeAdminLevel = (event) => {
    if (event.target.checked) {
      const selectedAdminLevel = parseInt(event.target.value);
      setAdminLevel(selectedAdminLevel);
      setGeoData(
        JSON.parse(vectorDataList[selectedAdminLevel - 1].geojson_str)
      );
    }
  };

  const changeSocioeconomicLayer = (event) => {
    if (event.target.checked) {
      const selectedSocioeconomicLayer = event.target.value;
      setVectorLayer(selectedSocioeconomicLayer);
    }
  };

  return (
    <div className="flex-container">
      <Dialog
        open={open}
        onClose={handleClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <DialogTitle>Choose two socioeconomic layers to analyze</DialogTitle>
        <DialogContent>
          <FormGroup>
            {vectorLayerList?.map((layer, index) => (
              <FormControlLabel
                sx={{
                  "& .MuiSvgIcon-root": {
                    fontSize: 15,
                  },
                  "& .MuiTypography-root": {
                    fontSize: 15,
                  },
                }}
                key={layer.name}
                value={layer.name}
                disabled={
                  vectorAnalyze.length >= 2 &&
                  vectorAnalyze.some((e) => e !== layer.name)
                }
                onChange={addVectorAnalyze}
                control={<Checkbox />}
                label={layer.description}
              />
            ))}
          </FormGroup>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleVectorAnalyze}>Analyze</Button>
        </DialogActions>
      </Dialog>
      <IconButton
        aria-label="vector-analyze"
        size="large"
        sx={{ position: "absolute", right: 0, zIndex: 999 }}
        onClick={handleOpen}
      >
        <TroubleshootOutlined fontSize="inherit" />
      </IconButton>
      <Grid>
        <SelectionPanel
          {...{
            adminLevel,
            changeAdminLevel,
            vectorLayer,
            changeSocioeconomicLayer,
            vectorLayerList,
          }}
        />
        <MapContainer
          center={[39, 70]}
          zoom={9}
          scrollWheelZoom={true}
          whenReady={(e) => {
            console.log(e);
            //e.target.flyToBounds([
            //[extent[1], extent[0]],
            //[extent[3], extent[2]]
            //]);
          }}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          <GeoJSONHandler
            {...{
              adminLevel,
              country,
              vectorLayer,
              setVectorDataList,
              setGeoJson,
              setGeoData,
              setCritiqueValue,
              geoJsonRef,
              geoData,
            }}
          />
        </MapContainer>
      </Grid>
    </div>
  );
}

export default MainPage;
