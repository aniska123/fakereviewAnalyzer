import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Signup.css';

function Signup() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:5000/signup', {
        username,
        password,
      });
      if (response.data.success) {
        setMessage('Signup successful! Redirecting to login...');
        setTimeout(() => navigate('/'), 2000);
      } else {
        setMessage(response.data.message);
      }
    } catch (error) {
      setMessage('Error connecting to server');
    }
  };

  return (
    <div className="signup-container">
      <div className="signup-box animate-slide-in">
        <h1>Fake Review Detector</h1>
        <h2>Sign Up</h2>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <button type="submit" className="animate-button">
            Sign Up
          </button>
        </form>
        {message && <p className="message">{message}</p>}
        <p>
          Already have an account? <Link to="/">Login</Link>
        </p>
      </div>
    </div>
  );
}

export default Signup;