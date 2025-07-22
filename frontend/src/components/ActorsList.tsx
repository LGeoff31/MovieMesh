import React, { useEffect, useState } from "react";

const ActorsList = () => {
  const [actors, setActors] = useState<{ actor_id: number; name: string }[]>([]);

  useEffect(() => {
    fetch("/api/actors/highest-grossing")
      .then(res => res.json())
      .then(setActors);
  }, []);

  return (
    <div>
      {actors.map(actor => (
        <div key={actor.actor_id} className="flex flex-col items-center justify-center">
          <h2>{actor.name}</h2>
        </div>
      ))}
    </div>
  );
};

export default ActorsList;