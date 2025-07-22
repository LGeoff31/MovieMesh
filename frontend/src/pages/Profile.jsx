import { useEffect, useState, useContext } from "react";
import { SearchContext } from "../components/SearchContext";
import { Link } from "react-router-dom";

export default function Profile() {
  const { user } = useContext(SearchContext);
  const [editMode, setEditMode] = useState(false);
  const [reviews, setReviews] = useState([]);

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
        <h1 className="text-5xl font-display font-bold ml-4">{user.name}</h1>
      </div>
      {reviews.length === 0 && <p>No reviews yet.</p>}
      <div className="flex justify-between">
        <h2 className="text-2xl font-display mb-4">My Reviews</h2>
        <button className="bg-blue-800 text-white m-2 px-2 py-1 rounded-md cursor-pointer hover:bg-blue-900" onClick={() => setEditMode(!editMode)}>{editMode ? "Save" : "Edit"}</button>
      </div>
      <ul className="space-y-3">
        {reviews.map((r) => (
          <Link to={`/movie/${r.movie_id}`} key={r.review_id}>
            <li className="p-4 border border-gray-200 rounded-lg">
                <span className="text-gray-700"> {r.title}: </span>
                <span className="font-bold">{r.rating}/10</span>
                <span className="ml-2 text-gray-700">– {r.comment_txt}</span>
                {editMode && (
                  <button className="bg-red-800 text-white float-right px-2 py-1 ml-2 rounded-md">Delete</button>
                )}
                <span className="float-right text-sm text-gray-400">{r.created_at}</span>
            </li>
          </Link>
        ))}
      </ul>
    </div>
  );
}