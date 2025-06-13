import { useEffect, useState } from 'react';
import { ListGroup } from 'react-bootstrap';

export default function ReviewList({ movieId }) {
  const [rev, setRev] = useState([]);

  useEffect(() => {
    fetch(`/api/movies/${movieId}/reviews`)
      .then(r => r.json()).then(setRev);
  }, [movieId]);

  return (
    <ListGroup>
      {rev.length === 0 && <ListGroup.Item>No reviews yet</ListGroup.Item>}
      {rev.map(r => (
        <ListGroup.Item key={r.review_id}>
          <b>{r.rating}/10</b> – {r.comment_txt}
          <span className="text-muted float-end">{r.created_at}</span>
        </ListGroup.Item>
      ))}
    </ListGroup>
  );
}
