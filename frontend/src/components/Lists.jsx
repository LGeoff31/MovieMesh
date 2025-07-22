import { Link } from "react-router-dom";

const Lists = () => {
  return (
    <div className="flex flex-row gap-4">
      <Link to="/analytics">Analytics</Link>
      <Link to="/lists/">Lists</Link>
    </div>
  )
}

export default Lists;