import { useState } from "react";
import { Link } from "react-router-dom";

export default function Search() {
  const [term, setTerm] = useState("");
  const [data, setData] = useState([]);

  const submit = (e) => {
    e.preventDefault();
    if (!term.trim()) return;
    fetch(`/api/search?q=${encodeURIComponent(term)}`)
      .then((r) => r.json())
      .then(setData);
  };

  return (
    <>
      <form onSubmit={submit} className="mb-6">
        <input
          type="text"
          value={term}
          onChange={(e) => setTerm(e.target.value)}
          placeholder="Search movies..."
          className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        />
      </form>

      <div className="space-y-2">
        {data.map((m) => (
          <div
            key={m.movie_id}
            className="flex items-center p-3 border border-gray-200 rounded-lg hover:bg-gray-50"
          >
            <img
              src={m.poster_link}
              width={40}
              className="mr-3 rounded"
              alt={m.title}
            />
            <Link 
              to={`/movie/${m.movie_id}`}
              className="flex-1 text-blue-600 hover:text-blue-800 no-underline"
            >
              {m.title} ({m.year})
            </Link>
            <span className="px-2 py-1 bg-gray-500 text-white text-sm rounded">
              {m.imdb_rating ?? ""}
            </span>
          </div>
        ))}
      </div>
    </>
  );
}
