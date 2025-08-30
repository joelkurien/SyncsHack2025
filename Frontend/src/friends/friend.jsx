import React, { useState } from 'react';
import './styleFriend.css';

function Friend({ onNavigate }) {
  const [friends, setFriends] = useState([
    { id: 1, username: 'alice' },
    { id: 2, username: 'bob' },
  ]);
  const [newUsername, setNewUsername] = useState('');

  const handleRemove = (id) => {
    setFriends(friends.filter((friend) => friend.id !== id));
  };

  const handleAdd = () => {
    if (!newUsername.trim()) return;

    const newFriend = {
      id: Date.now(),
      username: newUsername.trim(),
    };

    setFriends([...friends, newFriend]);
    setNewUsername('');
  };

  return (
    <div className = "friends">
    <div className="boxd">
      <h1 style = {{color: 'black'}}>Friends</h1>
      <table>
        <thead>
          <tr>
            <th className='fontstyle1'>ID</th>
            <th className='fontstyle1'>USERNAME</th>
            <th className='fontstyle1' >ACTION</th>
          </tr>
        </thead>
        <tbody>
          {friends.map((friend) => (
            <tr key={friend.id}>
              <td className='fontstyle2'>{friend.id}</td>
              <td className='fontstyle2' >{friend.username}</td>
              <td>
                <button className= 'btne' onClick={() => handleRemove(friend.id)}>Remove</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <div className="add-friend">
        <input
          type="text"
          placeholder="New friend's username"
          value={newUsername}
          onChange={(e) => setNewUsername(e.target.value)}
        />
        <button onClick={handleAdd}>Add Friend</button>
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

export default Friend;
