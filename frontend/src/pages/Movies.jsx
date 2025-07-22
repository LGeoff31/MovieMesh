import { useEffect, useState } from "react";
import RecentReviews from "../components/RecentReviews";
import TopMovies from "../components/TopMovies";

const Movies = () => {
  const [reviews, setReviews] = useState([]);

  useEffect(() => {
    fetch("/api/reviews/recent")
      .then(res => res.json())
      .then(setReviews);
  }, []);

  return (
    <div className="max-w-3xl mx-auto my-16">
      <RecentReviews />
      <TopMovies />
    </div>
  );
};

export default Movies;