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
    <div className="flex flex-col justify-start items-start my-4">
      <div className="flex flex-row items-center justify-start mb-4">
        <h1 className="text-3xl font-extrabold">FEATURED</h1>
        <p className="text-gray-500 ml-4">Our top picks for you</p>
      </div>
      <div className="flex flex-row items-start justify-start gap-4">
        {randomMovies && (
          randomMovies.map((movie) => (
            <div
                key={movie.movie_id}
                className="flex flex-col items-center p-5 border-2 bg-gray-100 border-gray-200 rounded-lg hover:bg-gray-50"
            >
              <Link 
                to={`/movie/${movie.movie_id}`}
                className="flex-1 no-underline"
              >
                <img
                  src={movie.poster_link}
                  width={200}
                  className="mr-3 rounded"
                  alt={movie.title}
                />
                <div className="flex flex-col items-start justify-start">
                  <p className="text-lg">{movie.title} <span className="text-gray-500 text-sm">({movie.year})</span></p>
                  <p className="px-2 py-1 bg-gray-500 text-white text-sm rounded">
                    {movie.imdb_rating ?? ""}
                  </p>
                </div>
              </Link>
            </div>
        )))}
      </div>
    </div>
  )
}

export default Featured;