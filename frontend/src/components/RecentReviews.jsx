import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

const RecentReviews = () => {
  const [reviews, setReviews] = useState([]);
  const colours = ["text-red-600", "text-red-600", "text-red-600", "text-orange-600", "text-orange-600", "text-orange-600", "text-yellow-600", "text-yellow-600", "text-green-700", "text-green-700", "text-green-700"]

  useEffect(() => {
    fetch("/api/reviews/recent-reviews")
      .then(r => r.json())
      .then(setReviews);

    console.log(reviews);
  }, []);
  
  return (
    <div className="flex flex-col justify-start items-start my-4 w-full">
      <div className="flex flex-row items-center justify-start mb-4">
        <h1 className="text-3xl font-extrabold">RECENT REVIEWS</h1>
        <p className="text-gray-500 ml-4">Latest reviews from our users</p>
      </div>
      <div className="flex flex-col items-start justify-start w-full">
        {reviews.map(review => (
          <Link to={`/movie/${review.movie_id}`} key={review.review_id} className="p-4 border border-gray-200 rounded-lg w-full">
            <div className="flex items-center gap-2">
              <img src={`/profile.jpg`} alt="Profile" className="w-10 h-10 rounded-full" />
              <span className="text-gray-700 font-bold">{review.username}</span>
              <span className="text-gray-500 text-sm">on {review.title}</span>
            </div>
            <div className="flex justify-between items-start gap-4">
              <div>
                <span className={`font-bold ${colours[Math.floor(review.rating)]}`}>{review.rating}/10</span>
                <span className="ml-2 text-gray-700">– {review.comment_txt}</span>
              </div>
              <span className="text-gray-400 text-sm">{review.created_at}</span>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default RecentReviews;