import { useState } from "react";
import "./Dashboard.css"

export default function Toolbar({ onNavigate }){

    const [user, setUser] = useState("Username");

    return (
        <header className="toolbar">
            <div className="left">NeoEco</div>

            <div className="right">
                <button onClick={() => onNavigate("friends")}>Friends</button>
                <button onClick={() => onNavigate("profile")}>Profile</button>
                <button onClick={() => onNavigate("login")}>Logout</button>
            </div>

        </header>

    
  );
}
