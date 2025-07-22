import { useEffect, useState } from "react";

const HighestGrossingActors = () => {
    const [actors, setActors] = useState([]);

    useEffect(() => {
        fetch("/api/actors/highest-grossing")
            .then(r => r.json())
            .then(setActors);
    }, []);

    return (
        <div className="flex flex-col justify-start items-start my-4 w-full">
            <div className="flex flex-row items-center justify-start mb-4">
                <h1 className="text-3xl font-extrabold">HIGHEST GROSSING ACTORS</h1>
                <p className="text-gray-500 ml-4">Top actors by total gross across all movies</p>
            </div>
            <ol className="list-decimal w-full">
              {actors.map(actor => {
                return (
                  <li key={actor.actor_id} className="flex flex-row items-center justify-between">
                    <h2 className="text-lg">{actor.name}</h2>
                    <p className="text-sm text-gray-500">${actor.total_gross.toLocaleString()}</p>
                  </li>
                )
              })}
            </ol>
        </div>
    )
}

export default HighestGrossingActors;