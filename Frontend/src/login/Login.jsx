import React, { useState } from 'react';
import './style.css'; //styling

function Login({ onLoginSuccess, onNavigate }) {

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();


  
    if (username === 'a' && password === 'p') { //remove it later
      setMessage('Login successful!');
      if (onLoginSuccess) onLoginSuccess();
     
    } else {
      setMessage('Invalid username or password.');
    }

  };

  return (
    <div className= 'login'>
    <div className="login-box">
      <h1>LOG IN</h1>
      <form onSubmit={handleSubmit}>

        <div className="login-textbox">
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div className="login-textbox">
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}

          />
        </div>
        <button className="btna" type="submit">Log In</button>

        <button
            className="btna"
            type="button"
            onClick={() => onNavigate?.('register')}
        >Register</button>

      </form>
      <p>{message}</p>
    </div>
    </div>
  );
}

export default Login;
