import { useState } from 'react';

export default function ReviewForm({ movieId, onSubmit }) {
  const [rating, setRating]   = useState('');
  const [comment, setComment] = useState('');

  const handle = (e) => {
    e.preventDefault();
    fetch(`/api/movies/${movieId}/reviews`, {
      method: 'POST',
      headers: { 'Content-Type':'application/json' },
      body: JSON.stringify({ rating:Number(rating), comment })
    }).then(r => r.ok && onSubmit());
  };

  return (
    <form onSubmit={handle} className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Rating (1-10)
        </label>
        <input 
          type="number" 
          min="1" 
          max="10"
          value={rating} 
          onChange={e=>setRating(e.target.value)} 
          required
          className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        />
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Comment
        </label>
        <textarea 
          rows={3}
          value={comment} 
          onChange={e=>setComment(e.target.value)} 
          required
          className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        />
      </div>
      <button 
        type="submit"
        className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition duration-200"
      >
        Submit
      </button>
    </form>
  );
}
