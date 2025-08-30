import React, { useState } from 'react';
import './style.css'; //styling

function Login({ onLoginSuccess, onNavigate }) {

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading]   = useState(false);
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');
    setLoading(true);

    try {
      const resp = await fetch('http://localhost:8000/user/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        // views.py expects { username, password } in request.data
        body: JSON.stringify({ username, password }),
      });

      // Parse JSON whether 200 or an error
      const data = await resp.json().catch(() => ({}));

      if (!resp.ok) {
        // Backend returns {"error": "..."} on failures
        const msg = data?.error || 'Login failed';
        setMessage(msg);
      } else {
        // On success, backend returns { message, token, user: {...} }
        const { token, user } = data || {};
        if (token) {
          // Store token for subsequent authenticated calls
          localStorage.setItem('authToken', token);
        }
        setMessage('Login successful!');
        // Let parent know (if needed to redirect or load profile)
        if (onLoginSuccess) onLoginSuccess({ token, user });
      }
    } catch (err) {
      console.error('Login error:', err);
      setMessage('Unable to reach server. Please try again.');
    } finally {
      setLoading(false);
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
