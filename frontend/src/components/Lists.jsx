import { Link } from "react-router-dom";

const Lists = () => {
  return (
    <div className="flex flex-row gap-4">
      <Link to="/lists/actors">Actors</Link>
      <Link to="/lists/movies">Movies</Link>
      <Link to="/lists/directors">Directors</Link>
    </div>
  )
}

export default Lists;