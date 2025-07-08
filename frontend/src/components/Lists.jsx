import { Link } from "react-router-dom";

const Lists = () => {
  return (
    <div className="flex flex-row gap-4">
      <Link to="/lists/actors">Actors</Link>
      <Link to="/lists/movies">Movies</Link>
    </div>
  )
}

export default Lists;