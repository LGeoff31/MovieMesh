import { Container, Navbar } from 'react-bootstrap';
import { Outlet, Link } from 'react-router-dom';

export default function App() {
  return (
    <>
      <Navbar bg="dark" variant="dark" className="mb-4">
        <Container>
          <Navbar.Brand as={Link} to="/">IMDB-Clone</Navbar.Brand>
        </Container>
      </Navbar>
      <Container>
        <Outlet />
      </Container>
    </>
  );
}
