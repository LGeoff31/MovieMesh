import { useState, useContext } from "react";
import { Link } from "react-router-dom";
import Navbar from "../components/Navbar";
import { SearchContext } from "../components/SearchContext";

export default function Search() {
  const {searchResults, setSearchResults} = useContext(SearchContext);

  return (
    <>
      <div className="space-y-2">
        {searchResults.map((m) => (
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
