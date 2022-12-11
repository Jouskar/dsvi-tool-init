import logo from './logo.svg';
import './App.css';
import TempMap from "./components/TempMap"
import reportWebVitals from './reportWebVitals';
import { MapContainer, TileLayer, Marker, Popup, GeoJSON } from 'react-leaflet';

function App() {
  /*return (
    <MapContainer center={[51.505, -0.09]} zoom={13} scrollWheelZoom={false}>
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <Marker position={[51.505, -0.09]}>
        <Popup>
          A pretty CSS3 popup. <br /> Easily customizable.
        </Popup>
      </Marker>
    </MapContainer>
  );*/
  return <TempMap/>;
}

export default App;
