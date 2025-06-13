import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { Row, Col, Spinner, Image, Badge, ListGroup } from "react-bootstrap";
import ReviewForm from "../components/ReviewForm";
import ReviewList from "../components/ReviewList";

export default function Movie() {
  const { id } = useParams();
  const [info, setInfo] = useState(null);

  useEffect(() => {
    fetch(`/api/movies/${id}`)
      .then((r) => r.json())
      .then(setInfo);
  }, [id]);

  if (!info) return <Spinner animation="border" />;

  const m = info.movie;

  return (
    <>
      <Link to="/">← Back</Link>

      {/* Header with poster & key facts */}
      <div className="d-flex my-3">
        <Image
          src={m.poster_link}
          alt={m.title}
          style={{ width: 140 }}
          rounded
          className="me-4"
        />
        <div>
          <h2>
            {m.title} ({m.year})
          </h2>

          <p className="mb-1">
            <Badge bg="info" className="me-2">
              {m.certificate || "NR"}
            </Badge>
            <span className="me-3">
              <strong>Runtime:</strong>{" "}
              {m.runtime_min ? `${m.runtime_min} min` : "N/A"}
            </span>
            <span>
              <strong>Gross:</strong>{" "}
              {m.gross_usd ? `$${(+m.gross_usd).toLocaleString()}` : "N/A"}
            </span>
          </p>

          <p className="mb-1">
            <strong>IMDB:</strong> {m.imdb_rating ?? "N/A"} |{" "}
            <strong>Metascore:</strong> {m.metascore ?? "N/A"}
          </p>
        </div>
      </div>

      <p>{m.overview}</p>

      <ListGroup horizontal className="mb-3">
        <ListGroup.Item>
          <strong>Directors:</strong> {info.directors.join(", ")}
        </ListGroup.Item>
        <ListGroup.Item>
          <strong>Cast:</strong> {info.cast.join(", ")}
        </ListGroup.Item>
        <ListGroup.Item>
          <strong>Genres:</strong> {info.genres.join(", ")}
        </ListGroup.Item>
      </ListGroup>

      <p>
        <em>
          {info.reviews_summary.num_reviews} user reviews, average{" "}
          {(info.reviews_summary.avg_rating || 0).toFixed(1)}
        </em>
      </p>

      <Row className="mt-4">
        <Col md={6}>
          <h4>User Reviews</h4>
          <ReviewList movieId={id} />
        </Col>
        <Col md={6}>
          <h4>Add Review</h4>
          <ReviewForm
            movieId={id}
            onSubmit={() => document.location.reload()}
          />
        </Col>
      </Row>
    </>
  );
}
