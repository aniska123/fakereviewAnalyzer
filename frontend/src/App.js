import React, { useState } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Signup from './components/Signup';
import ReviewAnalyzer from './components/ReviewAnalyzer';
import './App.css';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<Login setIsAuthenticated={setIsAuthenticated} />} />
        <Route path="/signup" element={<Signup />} />
        <Route
          path="/analyze"
          element={isAuthenticated ? <ReviewAnalyzer /> : <Navigate to="/" />}
        />
      </Routes>
    </div>
  );
}

export default App;