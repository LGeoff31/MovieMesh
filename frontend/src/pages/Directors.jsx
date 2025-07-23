import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

const Directors = () => {
  const [directors, setDirectors] = useState([]);

  useEffect(() => {
    fetch("/api/directors/top")
      .then(res => res.json())
      .then(setDirectors);
  }, []);

  return (
    <div className="max-w-3xl mx-auto my-16">
      <div className="flex flex-row items-center justify-start mb-4">
        <h1 className="text-3xl font-extrabold">TOP DIRECTORS</h1>
        <p className="text-gray-500 ml-4">Top directors by average rating across all movies</p>
      </div>
      <ul className="flex flex-col gap-2">
        {directors.map(director => (
          <li key={director.director_id} className="p-2 rounded-md border border-gray-300 hover:bg-gray-200">
            <Link to={`/directors/${director.director_id}`} className="flex flex-row items-center gap-2">
              <img src={'/profile.jpg'} alt="Avatar" className="w-12 h-12 rounded-full" />
              <p className="text-gray-700">{director.name}: {director.avg_rating} avg rating</p>
              <p className="text-gray-400 text-sm">({director.film_count} films)</p>
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Directors;