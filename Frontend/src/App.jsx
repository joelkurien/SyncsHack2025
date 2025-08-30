import { useState } from "react";
import './App.css'


import Login from "./login/Login";
import Toolbar from "./Dashboard/Toolbar";
import Score from "./Dashboard/Score"
import Task from "./Dashboard/Task"
import Challenge from "./Dashboard/Challenge"
import Friends from "./friends/friend";
import Profile from "./profile/Profile";
import RegistrationPage from "./registrationPage/page";

export default function App() {

    const [page, setPage] = useState("login");


    const renderPage = () => {
        switch (page) {
            case "dashboard":
                return (
                  <div className="dashboardBg">
                    <Toolbar onNavigate={setPage} />
                    <Score />
                    <Task />
                    <Challenge />
                  </div>
                );
            case "register":
                return <div className="registration"><RegistrationPage onNavigate={setPage} /></div>;
            case "friends":
                  return <Friends onNavigate={setPage} />;
            case "profile":
                  return <div className="Design"><Profile onNavigate={setPage} /></div>;
            default:
              return (
                <div className="homeDesign">
                <Login onLoginSuccess={() => setPage("dashboard")} onNavigate={setPage}
                /></div>
              );
        }
    };

    return (
    <>{renderPage()}</>
    );
}


