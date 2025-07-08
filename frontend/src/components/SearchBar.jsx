import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useContext } from "react";
import { SearchContext } from "./SearchContext";

const SearchBar = () => {
  const [term, setTerm] = useState("");
  const {searchResults, setSearchResults} = useContext(SearchContext);

  console.log(searchResults);

  const navigate = useNavigate();

  const submit = (e) => {
    e.preventDefault();
    if (!term.trim()) return;
    fetch(`/api/movies/search?q=${encodeURIComponent(term)}`)
      .then((r) => r.json())
      .then(setSearchResults);
    navigate(`/search?q=${encodeURIComponent(term)}`);
  };

  return (
    <div className="flex flex-col items-center justify-center w-1/2">
      <form onSubmit={submit} className="w-full">
        <input
          type="text"
          value={term}
          onChange={(e) => setTerm(e.target.value)}
          placeholder="Search movies..."
          className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        />
      </form>
    </div>
    
  )
}

export default SearchBar;