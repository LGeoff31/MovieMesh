import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

const Featured = () => {
  const [randomMovies, setRandomMovies] = useState(null);

  useEffect(() => {
    console.log("random movie");
    fetch("/api/movies/random")
      .then((r) => r.json())
      .then(setRandomMovies);
    console.log(randomMovies);
  }, []);

  return (
    <div className="flex flex-col items-center justify-center">
      <h1 className="text-2xl font-bold">Featured</h1>
      <div className="flex flex-row items-center justify-center">
        {randomMovies && (
          randomMovies.map((movie) => (
            <div
                key={movie.movie_id}
                className="flex flex-col items-center p-3 border border-gray-200 rounded-lg hover:bg-gray-50 w-1/2"
            >
              <Link 
                to={`/movie/${movie.movie_id}`}
                className="flex-1 text-blue-600 hover:text-blue-800 no-underline"
              >
                <img
                  src={movie.poster_link}
                  width={200}
                  className="mr-3 rounded"
                  alt={movie.title}
                />
                <div className="flex flex-row items-center justify-center">
                    {movie.title} ({movie.year})
                  <span className="px-2 py-1 bg-gray-500 text-white text-sm rounded">
                    {movie.imdb_rating ?? ""}
                  </span>
                </div>
              </Link>
            </div>
        )))}
      </div>
    </div>
  )
}

export default Featured;