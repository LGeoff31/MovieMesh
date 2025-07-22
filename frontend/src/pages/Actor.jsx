import { useParams, Link } from "react-router-dom";
import { useState, useEffect } from "react";

const Actor = () => {
  const {id} = useParams();
  const [actor, setActor] = useState(null);
  const [movies, setMovies] = useState([]);
  const [costars, setCostars] = useState([]);

  useEffect(() => {
    fetch(`/api/actors/${id}`)
      .then(res => res.json())
      .then(setActor);
  }, [id]);

  useEffect(() => {
    fetch(`/api/actors/${id}/movies`)
      .then(res => res.json())
      .then(setMovies);
  }, [id]);

  useEffect(() => {
    fetch(`/api/actors/${id}/costars`)
      .then(res => res.json())
      .then(setCostars);
  }, [id]);

  if (!actor) return <div>Loading...</div>;

  return (
    <div className="max-w-3xl mx-auto my-16">
      <div className="flex items-center my-4">
        <img src={'/profile.jpg'} alt="Avatar" className="w-24 h-24 rounded-full" />
        <div className="flex flex-col">
          <h1 className="text-5xl font-display font-bold ml-4 p-1">{actor.name}</h1>
          <h2 className="text-xl font-display ml-4 p-1">Total Gross: ${actor.total_gross.toLocaleString()}</h2>
        </div>
      </div>
      <div className="flex flex-col justify-start my-4">
        <h2 className="text-2xl font-display mb-4">Costars</h2>
        <ul className="flex flex-row flex-wrap gap-4">
          {costars.map((costar) => (
            <Link to={`/actors/${costar.actor_id}`} key={costar.actor_id}>
              <div className="flex flex-row items-center gap-2 p-2 rounded-md border border-gray-300 hover:bg-gray-200">
                <img src={'/profile.jpg'} alt="Avatar" className="w-12 h-12 rounded-full" />
                <p className="text-gray-700">{costar.name}</p>
              </div>
            </Link>
          ))}
        </ul>
      </div>
      <div className="flex flex-col">
        <h2 className="text-2xl font-display mb-4">Movies</h2>
        <ul className="flex flex-row flex-wrap gap-4">
          {movies.map((movie) => (
            <Link to={`/movie/${movie.movie_id}`} key={movie.movie_id}>
              <img
                src={movie.poster_link}
                alt={movie.title}
                className="rounded w-48"
              />
              <p className="text-gray-700 truncate w-48">{movie.title}</p>
              <p className="text-gray-400 text-sm">{movie.year}</p>
            </Link>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default Actor;