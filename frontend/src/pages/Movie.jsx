import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import ReviewForm from "../components/ReviewForm";
import ReviewList from "../components/ReviewList";

export default function Movie() {
  const { id } = useParams();
  const [info, setInfo] = useState(null);

  useEffect(() => {
    fetch(`/api/movies/${id}`)
      .then((r) => r.json())
      .then(setInfo);
  }, [id]);

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
          className="w-35 rounded mr-6"
          style={{ width: 140 }}
        />
        <div>
          <h2 className="text-3xl font-bold mb-4">
            {m.title} ({m.year})
          </h2>

          <p className="mb-2">
            <span className="inline-block bg-blue-500 text-white px-2 py-1 rounded text-sm mr-2">
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

          <p className="mb-2">
            <strong>IMDB:</strong> {m.imdb_rating ?? "N/A"} |{" "}
            <strong>Metascore:</strong> {m.metascore ?? "N/A"}
          </p>
        </div>
      </div>

      <p className="mb-6 text-gray-700">{m.overview}</p>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="p-4 border border-gray-200 rounded-lg">
          <strong>Directors:</strong> {info.directors.join(", ")}
        </div>
        <div className="p-4 border border-gray-200 rounded-lg">
          <strong>Cast:</strong> {info.cast.join(", ")}
        </div>
        <div className="p-4 border border-gray-200 rounded-lg">
          <strong>Genres:</strong> {info.genres.join(", ")}
        </div>
      </div>

      <p className="mb-6 italic text-gray-600">
        {info.reviews_summary.num_reviews} user reviews, average{" "}
        {(info.reviews_summary.avg_rating || 0).toFixed(1)}
      </p>

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
