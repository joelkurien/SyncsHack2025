import { useState } from "react";
import "./Dashboard.css"

export default function Toolbar(){

    const [user, setUser] = useState("User");

    return (
        <header className="toolbar">
            <div className="left">{user}</div>
            <div className="right">
                <a href="/profile">Profile</a>
                <a href="/logout">Logout</a>
            </div>

        </header>

    
  );
}
