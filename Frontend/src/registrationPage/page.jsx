
import React, { useState } from 'react';
import './Registrationstyle.css'; //styling

function Register({ onNavigate }) {
    const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [address1, setAddress1] = useState('');
  const [address2, setaddress2] = useState('');



  const handleRegister = (e) => {
    e.preventDefault();

    // TODO: Send registration data to backend here

    if (onNavigate) onNavigate("login");  // ⬅ go back to login page
  };



  
  return (
    <div className='registration'>
    <div className='boxc'>
        <h1 style = {{color: 'black'}}> REGISTER</h1>
        <form onSubmit={handleRegister}>
        <div className="mb-3">
          <input
            type="text"
            className="inputDesignb"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div className="mb-3">
          <input
            type="password"
            className="inputDesignb"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
         <div className="mb-3">
          <input
            type="Email"
            className="inputDesignb"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
         <div className="mb-3">
          <input
            type="address1"
            className="inputDesignb"
            placeholder="Home Adress"
            value={address1}
            onChange={(e) => setAddress1(e.target.value)}
            required
          />
        </div>
         <div className="mb-3">
          <input
            type="address2"
            className="inputDesignb"
            placeholder="Work Address"
            value={address2}
            onChange={(e) => setaddress2(e.target.value)}
            required
          />
        </div>
         
        <button className="btn" type="submit">CREATE</button>
      </form>

    </div>
    </div>
    
  );
}

export default Register;
