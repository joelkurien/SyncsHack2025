import { useEffect, useState, useRef } from "react";
import "./Dashboard.css"





function getSocialChallenges() {
  return [
    { id: 1, title: "quest11", description:"Hello", isDisplay: false },
    { id: 2, title: "quest12", description:"Hello", isDisplay: false },
    { id: 3, title: "quest13", description:"Hello", isDisplay: false }
  ];
}

function getVoluntierChallenges() {
  return [
    { id: 1, title: "quest21", description:"Hello", isDisplay: false },
    { id: 2, title: "quest22", description:"Hello", isDisplay: false },
    { id: 3, title: "quest23", description:"Hello", isDisplay: false }
  ];
}

function getCustomChallenges() {
  return [
    { id: 1, title: "quest31", description:"Hello", isDisplay: false },
    { id: 2, title: "quest32", description:"Hello", isDisplay: false },
    { id: 3, title: "quest33", description:"Hello", isDisplay: false }
  ];
}



export default function Challenge(){


  useEffect(() => {
    setSocialChallenges(getSocialChallenges());
    setVoluntierChallenges(getVoluntierChallenges());
    setCustomChallenges(getCustomChallenges());
  }, []);



  const [socialChallenges, setSocialChallenges] = useState([]);
  const [voluntierChallenges, setVoluntierChallenges] = useState([]);
  const [customChallenges, setCustomChallenges] = useState([]);


  
const socialIdFunction = (id) => {
  setSocialChallenges((prev) =>
    prev.map((c) =>
      c.id === id ? { ...c, isDisplay: !c.isDisplay } : c
    )
  );
};

const voluntierIdFunction = (id) => {
  setVoluntierChallenges((prev) =>
    prev.map((c) =>
      c.id === id ? { ...c, isDisplay: !c.isDisplay } : c
    )
  );
};

const customIdFunction = (id) => {
  setCustomChallenges((prev) =>
    prev.map((c) =>
      c.id === id ? { ...c, isDisplay: !c.isDisplay } : c
    )
  );
};






const fileInputRef = useRef(null);
const [uploadForId, setUploadForId] = useState(null);

const uploadFunction = (id) => {
  setUploadForId(id);
  if (fileInputRef.current) fileInputRef.current.click();
};

const handleFileChange = (e) => {
  const file = e.target.files?.[0];
  if (file) {
    console.log("Selected file:", file.name, "for challenge:", uploadForId);
    // TODO: upload to backend here
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


        <div className="challenge">
            <h2>Social Quests</h2>
            <ul className="sub-challenge">
                {socialChallenges.slice(0, 3).map((c) => (
                  <div className="sub-challenge-selected">


                  <div className="sub-challenge-heading">
                  <h3 key={c.id}>{c.title}</h3>               
                  <button className="button3"
              onClick={() => socialIdFunction(c.id)}
              >↴</button>
                </div>


                  {c.isDisplay && (
                  <div className="sub-challenge-bottom">
                      <p>Description: {c.description}</p>

                      <button className="button4"
                type="button"
                onClick={() => uploadFunction("current")}
                  >Completed</button>

                  
                  </div>
                  )}
                </div>
              ))}
            </ul>



            <h2>Voluntier Quests</h2>
            <ul className="sub-challenge">
                {voluntierChallenges.slice(0, 3).map((c) => (
                  <div className="sub-challenge-selected">


                  <div className="sub-challenge-heading">
                  <h3 key={c.id}>{c.title}</h3>               
                  <button className="button3"
              onClick={() => voluntierIdFunction(c.id)}
              >↴</button>
                </div>


                  {c.isDisplay && (
                  <div className="sub-challenge-bottom">
                      <p>Description: {c.description}</p>

                      <button className="button4"

                  >Accept</button>

                  
                  </div>
                  )}
                </div>
              ))}
            </ul>






            <h2>Custom Quests</h2>
            <ul className="sub-challenge">
                {customChallenges.slice(0, 3).map((c) => (
                  <div className="sub-challenge-selected">


                  <div className="sub-challenge-heading">
                  <h3 key={c.id}>{c.title}</h3>               
                  <button className="button3"
              onClick={() => customIdFunction(c.id)}
              >↴</button>
                </div>


                  {c.isDisplay && (
                  <div className="sub-challenge-bottom">
                      <p>Description: {c.description}</p>

                      <button className="button4"

                  >Accept</button>

                  
                  </div>
                  )}
                </div>
              ))}
            </ul>
        </div>
        </>
    );
}
