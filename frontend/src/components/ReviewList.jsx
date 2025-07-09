import { useEffect, useState } from 'react';

export default function ReviewList({ movieId }) {
  const [rev, setRev] = useState([]);
  const colours = ["text-red-600", "text-red-600", "text-red-600", "text-orange-600", "text-orange-600", "text-orange-600", "text-yellow-600", "text-yellow-600", "text-green-700", "text-green-700", "text-green-700"]
  
  useEffect(() => {
    fetch(`/api/movies/${movieId}/reviews`)
      .then(r => r.json()).then(setRev);
  }, [movieId]);

  return (
    <div className="space-y-3">
      {rev.length === 0 && (
        <div className="p-4 border border-gray-200 rounded-lg text-gray-500">
          No reviews yet
        </div>
      )}
      {rev.map(r => (
        <div key={r.review_id} className="p-4 border border-gray-200 rounded-lg">
          <div className="flex items-center gap-2">
            <img src={`/profile.jpg`} alt="Profile" className="w-10 h-10 rounded-full" />
            <span className="text-gray-700">{r.username}</span>
          </div>
          <div className="flex justify-between items-start gap-4">
            <div>
              <span className={`font-bold ${colours[Math.floor(r.rating)]}`}>{r.rating}/10</span>
              <span className="ml-2 text-gray-700">– {r.comment_txt}</span>
            </div>
            <span className="text-gray-400 text-sm">{r.created_at}</span>
          </div>
        </div>
      ))}
    </div>
  );
}
