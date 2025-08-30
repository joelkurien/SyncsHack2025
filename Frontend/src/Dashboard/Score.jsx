import "./Dashboard.css"


export default function Score(){



    const stat = {
        pic: "../assets/profile.webp",
        skill: "Bronze",
        xp: 7,
        level: 1
    };

    const leaderboard = [
        { ppl: "Alice", points: 20 },
        { ppl: "Bob", points: 22 },
        { ppl: "Charlie", points: 18 }
    ];



    return (
    <header className="score">

        <div className="score-left">
            <div className="first-row">
            <img className="level-image" src ={stat.pic}></img>
           <p>{stat.skill}</p>
            </div>
            <p>XP : {stat.xp}</p>
            <p>Level : {stat.level}</p>
        </div>


        <div className="score-right"><p>Leaderboard</p>
            <table className="leaderboard">

            <tr><th>Name</th><th>XP</th></tr>

                {leaderboard.slice(0, 3).map((leaderboard) => (
                    <tr><td>{leaderboard.ppl}</td><td>{leaderboard.points}</td></tr>
                  ))}


            </table>
        </div>

    </header>
  );
}
