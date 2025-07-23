import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

const TopMovies = () => {
    const [movies, setMovies] = useState([]);

    useEffect(() => {
        fetch("/api/movies/top")
            .then(r => r.json())
            .then(setMovies);
    }, []);

    return (
        <div className="flex flex-col justify-start items-start my-4 w-full">
            <div className="flex flex-row items-center justify-start mb-4">
                <h1 className="text-3xl font-extrabold">TOP MOVIES</h1>
                <p className="text-gray-500 ml-4">Top movies by average rating across all reviews</p>
            </div>
            <ol className="list-decimal w-full flex flex-col gap-2">
              {movies.map(movie => {
                return (
                  <li key={movie.movie_id} className="flex flex-row items-center justify-between p-2 rounded-md border border-gray-300 hover:bg-gray-200">
                    <Link to={`/movie/${movie.movie_id}`} className="flex flex-row items-center">
                      <img src={'/profile.jpg'} alt="Avatar" className="w-8 h-8 rounded-full" />
                      <h2 className="text-lg ml-4">{movie.title}</h2>
                    </Link>
                    <p className="text-lg font-bold">{movie.imdb_rating}</p>
                  </li>
                )
              })}
            </ol>
        </div>
    )
}

export default TopMovies;