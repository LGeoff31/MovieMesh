import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useContext } from "react";
import { SearchContext } from "./SearchContext";

const SearchBar = () => {
  const [term, setTerm] = useState("");
  const [searchTerm, setSearchTerm] = useState("");
  const {setSearchResults} = useContext(SearchContext);
  const [autocompleteResults, setAutocompleteResults] = useState([]);
  
  const navigate = useNavigate();

  const updateAutocomplete = (e) => {
    const newTerm = e.target.value;
    setTerm(newTerm);

    const stopwords = [
      "a", "an", "and", "are", "as", "at", "be", "but", "by",
      "for", "if", "in", "into", "is", "it", "no", "not",
      "of", "on", "or", "such", "that", "the", "their", "then",
      "there", "these", "they", "this", "to", "was", "will", "with",
    ];

    const filteredWords = newTerm
      .split(" ")
      .filter((word) => !stopwords.includes(word.toLowerCase()) && word.length > 3);
    const filteredTerm = filteredWords.join(" ");

    if (!filteredTerm.trim()) {
      setAutocompleteResults([]);
      return;
    }

    if (filteredTerm !== searchTerm) {
      fetch(`/api/movies/autocomplete?q=${encodeURIComponent(filteredTerm)}`)
        .then((r) => r.json())
        .then(setAutocompleteResults);
      setSearchTerm(filteredTerm);
    }
  };

  const submit = (e) => {
    e.preventDefault();
    if (!term.trim()) return;
    fetch(`/api/movies/search?q=${encodeURIComponent(term)}`)
      .then((r) => r.json())
      .then(setSearchResults)
      .then(() => setAutocompleteResults([]));
    navigate(`/search?q=${encodeURIComponent(term)}`);
  };

  return (
    <div className="flex flex-col items-center justify-center w-1/2">
      <form onSubmit={submit} className="w-full">
        <input
          type="text"
          value={term}
          onChange={updateAutocomplete}
          onBlur={() => setAutocompleteResults([])}
          placeholder="Search movies..."
          className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        />
        {term && (
          <ul className="absolute w-1/2 mt-1 bg-slate-800 rounded-md shadow-lg z-10">
            {autocompleteResults.map((result) => (
              <Link to={`/movie/${result.movie_id}`} key={result.movie_id} onClick={() => setAutocompleteResults([])}>
                <li className="px-3 py-2 hover:bg-gray-700 cursor-pointer">{result.title}</li>
              </Link>
            ))}
          </ul>
        )}
      </form>
    </div>
    
  )
}

export default SearchBar;