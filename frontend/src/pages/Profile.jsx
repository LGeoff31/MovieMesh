import { useEffect, useState, useContext } from "react";
import { SearchContext } from "../components/SearchContext";
import { Link } from "react-router-dom";

export default function Profile() {
  const { user } = useContext(SearchContext);
  const [editMode, setEditMode] = useState(false);
  const [reviews, setReviews] = useState([]);

  const handleDelete = (reviewId) => {
    const token = localStorage.getItem("token");
    console.log(reviewId);
    fetch(`/api/reviews/${reviewId}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    });
    setReviews(reviews.filter((r) => r.review_id !== reviewId));
  };

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) return;

    const fetchReviews = async () => {
      const res = await fetch("/api/users/me/reviews", {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (res.ok) {
        const data = await res.json();
        setReviews(data);
      }
    };

    fetchReviews();
  }, []);

  if (!user) {
    return <p className="text-center mt-8">Please log in to see your profile.</p>;
  }

  return (
    <div className="max-w-3xl mx-auto mt-8">
      <div className="flex items-center my-16">
        <img src={'/profile.jpg'} alt="Avatar" className="w-24 h-24 rounded-full" />
        <div className="flex flex-col">
          <h1 className="text-5xl font-display font-bold ml-4">{user.name}</h1>
          <h2 className="text-2xl font-display ml-4">{user.username}</h2>
        </div>
      </div>
      <div className="flex justify-between">
        <h2 className="text-2xl font-display mb-4">My Reviews</h2>
        {reviews.length > 0 && <button className="bg-blue-800 text-white m-2 px-2 py-1 rounded-md cursor-pointer hover:bg-blue-900" onClick={() => setEditMode(!editMode)}>{editMode ? "Save" : "Edit"}</button>}
      </div>
      {reviews.length === 0 && <p>No reviews yet.</p>}
      <ul className="space-y-3">
        {reviews.map((r) => (
          <div key={r.review_id} className="p-4 border border-gray-200 rounded-lg flex justify-between items-center">
            <Link to={`/movie/${r.movie_id}`} key={r.review_id}>
            <p className="text-xs text-gray-400">{r.created_at}</p>
            <p className="text-gray-700">
              {r.title}: <span className="font-bold">{r.rating}/10 </span>
              – {r.comment_txt}
            </p>
            </Link>
            {editMode && (
              <button className="bg-red-800 text-white px-2 h-8 rounded-md cursor-pointer hover:bg-red-900" onClick={() => handleDelete(r.review_id)}>Delete</button>
            )}
          </div>
        ))}
      </ul>
    </div>
  );
}