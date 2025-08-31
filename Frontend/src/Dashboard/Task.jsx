import { useState, useRef } from "react";
import "./Dashboard.css"

export default function Task(){

    const [current, setCurrent] = useState({
    title: "Quest Demo",
    description: "Desc Hello"});

    const [isDisplay, setIsDisplay] = useState(false);






const fileInputRef = useRef(null);
const [uploadForId, setUploadForId] = useState(null);

const [isUploaded, setIsUploaded] = useState(false);

const uploadFunction = (id) => {
    setUploadForId(id);
    if (fileInputRef.current) fileInputRef.current.click();
};

const handleFileChange = (e) => {
    const file = e.target.files?.[0];
    if (file) {
        console.log("Selected file:", file.name, "for challenge:", uploadForId);
        setIsUploaded(true);
      }
      e.target.value = ""; // reset so selecting the same file again re-triggers change
};


    

    return (
        <>
        <input
        type="file"
        ref={fileInputRef}
        style={{ display: "none" }}
        onChange={handleFileChange}
        />


        <header className="task">
            <div className="task-top">
                <div className="task-left">Curent Group Task: {current.title}</div>

                <button className="button"
                onClick={() => setIsDisplay(!isDisplay)}
                >↴</button>

            </div>


            {isDisplay && (
            <div className="task-bottom">
                <p>Description: {current.description}</p>


            <div>
            {!isUploaded && (
            <button className="button5"
                type="button"
                onClick={() => uploadFunction("current")}
            >Upload</button>)}

            <button className="button2">Decline</button>
            </div>

          
            </div>
            )}

        </header></>
    );
}
