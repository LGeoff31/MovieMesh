import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Row, Col, ListGroup, Spinner } from 'react-bootstrap';
import ReviewForm from '../components/ReviewForm';
import ReviewList from '../components/ReviewList';

export default function Movie() {
  const { id } = useParams();
  const [info, setInfo] = useState(null);

  useEffect(() => {
    fetch(`/api/movies/${id}`).then(r => r.json()).then(setInfo);
  }, [id]);

  if (!info) return <Spinner animation="border" />;

  const m = info.movie;
  return (
    <>
      <Link to="/">← Back</Link>
      <h2 className="mt-2">{m.title} ({m.year})</h2>
      <p>{m.overview}</p>
      <p><b>IMDB:</b> {m.imdb_rating} | <b>Metascore:</b> {m.metascore}</p>
      <p><b>Directors:</b> {info.directors.join(', ')}</p>
      <p><b>Cast:</b> {info.cast.join(', ')}</p>
      <p><b>Genres:</b> {info.genres.join(', ')}</p>
      <p><i>{info.reviews_summary.num_reviews} reviews – average {(info.reviews_summary.avg_rating||0).toFixed(1)}</i></p>

      <Row className="mt-4">
        <Col md={6}>
          <h4>User Reviews</h4>
          <ReviewList movieId={id} />
        </Col>
        <Col md={6}>
          <h4>Add Review</h4>
          <ReviewForm movieId={id} onSubmit={() => document.location.reload()} />
        </Col>
      </Row>
    </>
  );
}
