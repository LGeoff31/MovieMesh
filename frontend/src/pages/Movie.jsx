import { useEffect, useState, useContext } from "react";
import { useParams, Link } from "react-router-dom";
import ReviewForm from "../components/ReviewForm";
import ReviewList from "../components/ReviewList";
import { SearchContext } from "../components/SearchContext";

export default function Movie() {
  const { id } = useParams();
  const [info, setInfo] = useState(null);
  const [userRating, setUserRating] = useState(null);
  const [ratingChart, setRatingChart] = useState([]);
  const [showChart, setShowChart] = useState(false);
  const {user} = useContext(SearchContext);

  const colours = ["bg-red-600 border-red-600", "bg-red-600 border-red-600", "bg-red-600 border-red-600", "bg-orange-600 border-orange-600", "bg-orange-600 border-orange-600", "bg-orange-600 border-orange-600", "bg-yellow-600 border-yellow-600", "bg-yellow-600 border-yellow-600", "bg-green-700 border-green-700", "bg-green-700 border-green-700"]

  useEffect(() => {
    fetch(`/api/movies/${id}`)
      .then((r) => r.json())
      .then(setInfo);
  }, [id]);

  useEffect(() => {
    fetch(`/api/movies/${id}/rating_chart`)
      .then((r) => r.json())
      .then(setRatingChart);
  }, [id]);

  useEffect(() => {
    if (user) {
      fetch(`/api/movies/${id}/rating_by_user/${user.user_id}`)
        .then((r) => r.json())
        .then((data) => setUserRating(data ?? null));
    }
  }, [id, user]);

  if (!info) return (
    <div className="flex justify-center items-center h-32">
      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
    </div>
  );

  const m = info.movie;

  return (
    <>
      <Link to="/" className="text-blue-600 hover:text-blue-800 no-underline">← Back</Link>

      {/* Header with poster & key facts */}
      <div className="flex my-6">
        <img
          src={m.poster_link}
          alt={m.title}
          className="w-1/4 rounded mr-6"
        />
        <div className="flex flex-col justify-start w-full">
          <div className="flex flex-row items-center justify-between">
            <div>
              <h1 className="text-5xl font-bold mb-2">
                {m.title}
              </h1>
              <p className="mb-2">
                <span className="inline-block bg-blue-800 text-white px-2 py-1 rounded text-sm mr-2">
                  {m.certificate || "NR"}
                </span>
                <span className="mr-6">
                  <strong>Runtime:</strong>{" "}
                  {m.runtime_min ? `${m.runtime_min} min` : "N/A"}
                </span>
                <span>
                  <strong>Gross:</strong>{" "}
                  {m.gross_usd ? `$${(+m.gross_usd).toLocaleString()}` : "N/A"}
                </span>
              </p>
            </div>

            <div className="mb-2 flex flex-row items-center gap-4">
              <div className="flex flex-col items-center border-2 border-gray-500 text-black rounded-lg py-2 px-4">
                <p className="text-sm">Your Rating</p>
                <p className="text-4xl font-black">{userRating ?? "N/A"}</p>
              </div>
              <div
                className={`relative flex flex-col items-center border-2 border-blue-900 ${colours[Math.floor(m.imdb_rating)]} text-white rounded-lg py-2 px-4`}
                onMouseEnter={() => setShowChart(true)}
                onMouseLeave={() => setShowChart(false)}
              >
                <p className="text-sm">MovieMesh</p>
                <p className="text-4xl font-black">{m.imdb_rating ?? "N/A"}</p>
                {showChart && (
                  <div className="absolute left-0 top-24 mt-2 bg-white text-black border border-gray-400 rounded shadow-lg p-2 z-20 w-64">
                    <h4 className="text-center font-semibold mb-2">Rating Distribution</h4>
                    {ratingChart.map((b, index) => (
                      <div key={index} className="flex items-center mb-1">
                        <span className="w-6 text-sm">{index + 1}</span>
                        <div className="flex-1 bg-gray-300 h-3 mx-2 rounded">
                          <div
                            className="bg-blue-600 h-3 rounded"
                            style={{ width: `${(b / Math.max(...ratingChart)) * 100}%` }}
                          ></div>
                        </div>
                        <span className="w-8 text-xs text-right">{b}</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
          <div className="py-3 m-1 flex flex-row gap-2">
            {info.genres.map((genre) => (
              <div className="px-3 py-1 border border-gray-400 rounded-3xl" key={genre}>
                {genre}
              </div>
            ))}
          </div>
          <div className="p-3 m-1 border border-gray-400 rounded-lg">
            <strong>Directors:</strong> {info.directors.join(", ")}
          </div>
          <div className="p-3 m-1 border border-gray-400 rounded-lg">
            <strong>Cast:</strong> {info.cast.join(", ")}
          </div>
          <p className="m-1 py-2 text-lg text-gray-700">{m.overview}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mt-8">
        <div>
          <h4 className="text-xl font-semibold mb-4">User Reviews</h4>
          <ReviewList movieId={id} />
        </div>
        <div>
          <h4 className="text-xl font-semibold mb-4">Add Review</h4>
          <ReviewForm
            movieId={id}
            onSubmit={() => document.location.reload()}
          />
        </div>
      </div>
    </>
  );
}
