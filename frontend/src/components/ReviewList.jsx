import { useEffect, useState } from 'react';

export default function ReviewList({ movieId }) {
  const [rev, setRev] = useState([]);

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
          <div className="flex justify-between items-start">
            <div>
              <span className="font-bold text-blue-600">{r.rating}/10</span>
              <span className="ml-2 text-gray-700">– {r.comment_txt}</span>
            </div>
            <span className="text-gray-400 text-sm">{r.created_at}</span>
          </div>
        </div>
      ))}
    </div>
  );
}
