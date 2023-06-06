import React from 'react';
import { createBrowserRouter, BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './Login/Login';
import MainPage from './MainPage';

const router = createBrowserRouter([
  {path: '/', element: <MainPage/>}
])

const App = () => {
  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<MainPage/>} />
        <Route path="/login" element={<Login/>} />
      </Routes>
    </Router>
  );
};

export default App;
