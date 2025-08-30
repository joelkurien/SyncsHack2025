import React from 'react';
import './stylingProfile.css';

function Profile({ onNavigate }) {
  const username = "admin";
  const email = "email@gmail.com"
  const XP = "100";
  const skill = "GOld";
  const address1 = "glebe";
  const address2 = "USYD";
  const city = "SYDNEY";
  const state = "NSW";

  return (
    <div className="Design">
      <div className = "boxb">
        <h1 style = {{color: 'black'}}> PROFILE</h1>
         <div className = 'label-row'>
          <label className='label1'>Username  :  </label>  
         <label className='label2'> {username}  </label> 
         </div>
          <div className = 'label-row'>
          <label className='label1'>Email  :  </label>  
         <label className='label2'> {email}  </label> 
         </div>
          <div className = 'label-row'>
          <label className='label1'>XP  :  </label>  
         <label className='label2'> {XP}  </label> 
         </div>
          <div className = 'label-row'>
          <label className='label1'>Skill  :  </label>  
         <label className='label2'> {skill}  </label> 
         </div>
          <div className = 'label-row'>
          <label className='label1'>Home address  :  </label>  
         <label className='label2'> {address1}  </label> 
         </div>
          <div className = 'label-row'>
          <label className='label1'>Work Address  :  </label>  
         <label className='label2'> {address2}  </label> 
         </div>
          <div className = 'label-row'>
          <label className='label1'>City :  </label>  
         <label className='label2'> {city}  </label> 
         </div>
          <div className = 'label-row'>
          <label className='label1'>State  :  </label>  
         <label className='label2'> {state}  </label> 
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
