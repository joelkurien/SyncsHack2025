import React, { useEffect, useState } from 'react';
import './stylingProfile.css';

function Profile({ onNavigate }) {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {

    fetch('http://localhost:8000/user/profile', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(async (res) => {
        if (!res.ok) {
          const text = await res.text();
          throw new Error(text || 'Failed to fetch profile');
        }
        return res.json();
      })
      .then((data) => {
        setProfile(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading profile...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="Design">
      <div className = "boxb">
        <h1 style = {{color: 'black'}}> PROFILE</h1>
         <div className = 'label-row'>
          <label className='label1'>Username  :  </label>  
         <label className='label2'> {profile.username}  </label> 
         </div>
          <div className = 'label-row'>
          <label className='label1'>Email  :  </label>  
         <label className='label2'> {profile.email}  </label> 
         </div>
          <div className = 'label-row'>
          <label className='label1'>XP  :  </label>  
         <label className='label2'> {profile.xp}  </label> 
         </div>
          <div className = 'label-row'>
          <label className='label1'>Home address  :  </label>  
         <label className='label2'> {profile.address}  </label> 
         </div>
          <div className = 'label-row'>
          <label className='label1'>Work Address  :  </label>  
         <label className='label2'> {profile.work_address}  </label> 
         </div>
         
        <div className="buttonf">
        <button className="btn" onClick={() => onNavigate("dashboard")}>
            Back to Dashboard
        </button>
      </div>
               
     

      </div>
      
    </div>
  );
}

export default Profile;
