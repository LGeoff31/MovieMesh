import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";

const ActorsSearch = () => {
  const [search, setSearch] = useState("");
  const [results, setResults] = useState([]);

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    fetch(`/api/actors/search?q=${search}`)
      .then(res => res.json())
      .then(setResults);
    setSearch("");
    console.log(results);
  };

  return (
    <div className="flex flex-col justify-start items-start my-4 w-full">
      <div className="flex flex-row items-center justify-start mb-4">
          <h1 className="text-3xl font-extrabold">ACTOR SEARCH</h1>
          <p className="text-gray-500 ml-4">Search for an actor by name</p>
      </div>
      <form onSubmit={handleSubmit} className="flex flex-row items-center justify-start mb-4 w-full">
        <input
          type="text"
          placeholder="Search for an actor"
          value={search}
          onChange={e => setSearch(e.target.value)}
          className="border border-gray-400 rounded-md p-2 w-1/2"
        />
      </form>
      {results.map((result: {actor_id: number, name: string}) => (
        <Link to={`/actors/${result.actor_id}`} key={result.actor_id} onClick={() => setResults([])}>
          <h2>{result.name}</h2>
        </Link>
      ))}
    </div>
  );
};

export default ActorsSearch;