import { useEffect, useState } from "react";

const HighestGrossingActors = () => {
    const [actors, setActors] = useState([]);

    useEffect(() => {
        fetch("/api/actors/highest-grossing")
            .then(r => r.json())
            .then(setActors);
    }, []);

    return (
        <div>
            <h1 className="text-2xl font-bold">Highest Grossing Actors</h1>
            {actors.map(actor => {
              return (
                <div key={actor.actor_id} className="flex flex-row items-center justify-between">
                  <h2 className="text-lg">{actor.name}</h2>
                  <p className="text-sm text-gray-500">${actor.total_gross.toLocaleString()}</p>
                </div>
              )
            })}
        </div>
    )
}

export default HighestGrossingActors;