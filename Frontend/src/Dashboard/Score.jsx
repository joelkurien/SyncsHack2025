// Score.jsx
import React, { useEffect, useState } from "react";
import "./Dashboard.css";
import Bronze from "../assets/Bronze.jpg";
import Silver from "../assets/Silver.jpg";
import Gold from "../assets/Gold.jpg";
import Master from "../assets/Master.jpg";

const images = { Bronze, Silver, Gold, Master };

function xpToLevel(xp) {
  return Math.max(1, Math.floor((xp ?? 0) / 100) + 1);
}
function levelToSkill(level) {
  if (level >= 10) return "Master";
  if (level >= 7) return "Gold";
  if (level >= 4) return "Silver";
  return "Bronze";
}

export default function Score() {
  const [stat, setStat] = useState({ skill: "Bronze", xp: 0, level: 1 });
  const [leaderboard, setLeaderboard] = useState([]);

  useEffect(() => {
    async function load() {
      // 1) Profile for current XP
      const profileRes = await fetch("http://localhost:8000/user/profile");
      const profile = await profileRes.json();

      const level = xpToLevel(profile?.xp ?? 0);
      const skill = levelToSkill(level);

      setStat({ xp: profile?.xp ?? 0, level, skill });

      // 2) Leaderboard (friends)
      const lbRes = await fetch("http://localhost:8000/user/leaderboard");
      const lb = await lbRes.json();
      setLeaderboard(lb?.leaderboard ?? []);
    }

    load().catch(console.error);
  },[]);

  return (
    <header className="score">

        <div className="score-left">
            <div className="first-row">
            <img 
            className="level-image" 
            src={images[stat.skill]}/>
           <p>{stat.skill}</p>
            </div>
            <p>XP : {stat.xp}</p>
            <p>Level : {stat.level}</p>
        </div>


        <div className="score-right"><p>Leaderboard</p>
            <table className="leaderboard">

            <tr><th>Name</th><th>XP</th></tr>

                {leaderboard.slice(0, 3).map((leaderboard) => (
                    <tr><td>{leaderboard.username}</td><td>{leaderboard.xp}</td></tr>
                  ))}


            </table>
        </div>

    </header>
  );
}
