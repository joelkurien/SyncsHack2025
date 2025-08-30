import { useEffect, useState, useRef } from "react";
import "./Dashboard.css";

function getSocialChallenges() {
  return [
    { id: 1, title: "quest11", description: "Hello", isDisplay: false },
    { id: 2, title: "Recycle Bottles", description: "Try to recycle at least 5 bottles", isDisplay: false },
    { id: 3, title: "Plant Trees", description: "Try to plant at least 5 trees", isDisplay: false }
  ];
}

function getVolunteerChallenges() {
  return [
    { id: 1, title: "quest21", description: "Hello", isDisplay: false },
    { id: 2, title: "quest22", description: "Hello", isDisplay: false },
    { id: 3, title: "quest23", description: "Hello", isDisplay: false }
  ];
}

function getCustomChallenges() {
  return [
    { id: 1, title: "Clean the Beach", description: "Hello", isDisplay: false },
    { id: 2, title: "Afforest a sanctuary", description: "Hello", isDisplay: false },
    { id: 3, title: "Recycle Waste Materials", description: "Hello", isDisplay: false }
  ];
}

const toTitle = (s) => {
  const t = String(s || "").trim();
  return t ? t[0].toUpperCase() + t.slice(1).toLowerCase() : "";
};

const actionDescription = (pretty) => {
  switch (pretty) {
    case "Walk": return "Walk to work today (or hit 3,000 extra steps).";
    case "Bicycle": return "Bike to work and save some CO₂!";
    case "Bus": return "Take the bus for at least one leg of your commute.";
    case "Train": return "Use the train for your commute today.";
    case "Take A Car": return "If needed, carpool or combine errands to reduce trips.";
    default: return `Try to ${pretty.toLowerCase()} to work today.`;
  }
};

export default function Challenge() {
  const [socialChallenges, setSocialChallenges] = useState([]);
  const [volunteerChallenges, setVolunteerChallenges] = useState([]);
  const [customChallenges, setCustomChallenges] = useState([]);
  const fileInputRef = useRef(null);
  const [uploadForId, setUploadForId] = useState(null);

  useEffect(() => {
    // Seed initial lists
    setSocialChallenges(getSocialChallenges());
    setVolunteerChallenges(getVolunteerChallenges());
    setCustomChallenges(getCustomChallenges());

    // Fetch transport recommendation and prepend as a Social quest
    (async () => {
      try {
        const resp = await fetch("http://localhost:8000/quests/transport", {
          method: "GET",
          headers: { "Content-Type": "application/json" }
        });
        const data = await resp.json();

        // accept either { decision: { action: "walk" } } or { decision: "walk" }
        const rawAction =
          data?.decision?.action ??
          (typeof data?.decision === "string" ? data.decision : "walk");

        const pretty = toTitle(rawAction || "walk"); // e.g., "Walk"
        const newChallenge = {
          id: "transport", // stable synthetic id
          title: pretty,   // <-- title equals transport decision
          description: actionDescription(pretty),
          isDisplay: false
        };

        setSocialChallenges(prev =>
          prev.length ? [newChallenge, ...prev.slice(1)] : [newChallenge]
        );
      } catch (e) {
        console.error("Transport decision fetch failed:", e);
        const pretty = "Walk";
        const fallback = {
          id: "transport-fallback",
          title: pretty,
          description: actionDescription(pretty),
          isDisplay: false
        };
        setSocialChallenges(prev =>
          prev.length ? [fallback, ...prev.slice(1)] : [fallback]
        );
      }
    })();

    // Fetch volunteer opportunities
    (async () => {
      try {
        const resp = await fetch("http://localhost:8000/quests/volunteer", {
          method: "GET",
          headers: { "Content-Type": "application/json" }
        });
        const data = await resp.json();
        const volunteerData =
          data?.results?.slice(0, 3).map((item, index) => ({
            id: `volunteer-${index}`,
            title: item.title,
            description: item.description,
            isDisplay: false
          })) ?? getVolunteerChallenges();
        setVolunteerChallenges(volunteerData);
      } catch (e) {
        console.error("Volunteer fetch failed:", e);
        setVolunteerChallenges(getVolunteerChallenges()); // fallback
      }
    })();
  }, []);

  const toggleSocial = (id) => {
    setSocialChallenges(prev =>
      prev.map(c => (c.id === id ? { ...c, isDisplay: !c.isDisplay } : c))
    );
  };

  const toggleVolunteer = (id) => {
    setVolunteerChallenges(prev =>
      prev.map(c => (c.id === id ? { ...c, isDisplay: !c.isDisplay } : c))
    );
  };

  const toggleCustom = (id) => {
    setCustomChallenges(prev =>
      prev.map(c => (c.id === id ? { ...c, isDisplay: !c.isDisplay } : c))
    );
  };

  const uploadFunction = (id) => {
    setUploadForId(id);
    if (fileInputRef.current) fileInputRef.current.click();
  };

  const handleFileChange = async (e) => {
    const file = e.target.files?.[0];
    if (!file) {
      e.target.value = "";
      return;
    }

    try {
      const formData = new FormData();
      formData.append("file", file);
      if (uploadForId) formData.append("quest_id", String(uploadForId));

      const resp = await fetch("http://localhost:8000/quests/complete_quest", {
        method: "POST",
        body: formData
      });

      const result = await resp.json();
      if (!resp.ok) {
        console.error("Upload failed:", result);
        alert(result?.error || "Upload failed");
      } else {
        console.log("Upload ok:", result);
        alert(`Completed! +${result?.xp_gain ?? 0} XP`);
      }
    } catch (err) {
      console.error("Upload error:", err);
      alert("Upload error");
    } finally {
      e.target.value = ""; // reset so selecting the same file again re-triggers change
    }
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
            <li className="sub-challenge-selected" key={c.id}>
              <div className="sub-challenge-heading">
                <h3>{c.title}</h3>
                <button className="button3" onClick={() => toggleSocial(c.id)}>↴</button>
              </div>
              {c.isDisplay && (
                <div className="sub-challenge-bottom">
                  <p>Description: {c.description}</p>
                  <button
                    className="button4"
                    type="button"
                    onClick={() => uploadFunction(c.id)}
                  >
                    Completed
                  </button>
                </div>
              )}
            </li>
          ))}
        </ul>

        <h2>Volunteer Quests</h2>
        <ul className="sub-challenge">
          {volunteerChallenges.slice(0, 3).map((c) => (
            <li className="sub-challenge-selected" key={c.id}>
              <div className="sub-challenge-heading">
                <h3>{c.title}</h3>
                <button className="button3" onClick={() => toggleVolunteer(c.id)}>↴</button>
              </div>
              {c.isDisplay && (
                <div className="sub-challenge-bottom">
                  <p>Description: {c.description}</p>
                  <button className="button4">Accept</button>
                </div>
              )}
            </li>
          ))}
        </ul>

        <h2>Custom Quests</h2>
        <ul className="sub-challenge">
          {customChallenges.slice(0, 3).map((c) => (
            <li className="sub-challenge-selected" key={c.id}>
              <div className="sub-challenge-heading">
                <h3>{c.title}</h3>
                <button className="button3" onClick={() => toggleCustom(c.id)}>↴</button>
              </div>
              {c.isDisplay && (
                <div className="sub-challenge-bottom">
                  <p>Description: {c.description}</p>
                  <button className="button4">Accept</button>
                </div>
              )}
            </li>
          ))}
        </ul>
      </div>
    </>
  );
}
