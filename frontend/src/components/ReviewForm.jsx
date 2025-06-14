import { useState } from 'react';
import { Form, Button } from 'react-bootstrap';

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
    <Form onSubmit={handle}>
      <Form.Group className="mb-2">
        <Form.Label>Rating (1-10)</Form.Label>
        <Form.Control type="number" min="1" max="10"
          value={rating} onChange={e=>setRating(e.target.value)} required/>
      </Form.Group>
      <Form.Group className="mb-2">
        <Form.Label>Comment</Form.Label>
        <Form.Control as="textarea" rows={3}
          value={comment} onChange={e=>setComment(e.target.value)} required/>
      </Form.Group>
      <Button type="submit">Submit</Button>
    </Form>
  );
}
