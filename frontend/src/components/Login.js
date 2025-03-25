import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Login.css';

function Login({ setIsAuthenticated }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:5000/login', {
        username,
        password,
      });
      if (response.data.success) {
        setIsAuthenticated(true);
        navigate('/analyze');
      } else {
        setMessage(response.data.message);
      }
    } catch (error) {
      setMessage('Error connecting to server');
    }
  };

  return (
    <div className="login-container">
      <div className="login-box animate-slide-in">
        <h1>Fake Review Detector</h1>
        <h2>Login</h2>
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
            Login
          </button>
        </form>
        {message && <p className="message">{message}</p>}
        <p>
          Don't have an account? <Link to="/signup">Sign up</Link>
        </p>
      </div>
    </div>
  );
}

export default Login;