import { Link, useLocation } from "react-router-dom";
import SearchBar from "./SearchBar";
import Lists from "./Lists";

const Navbar = () => {

  const location = useLocation();
  const isLoginPage = location.pathname === "/login";
  
  return (
    <nav className="w-full bg-gray-900 text-white mb-4">
      <div className="w-full mx-auto px-4 sm:px-6 lg:px-8">
      <div className="w-full flex items-center h-16 justify-between">
        <Link to="/" className="text-3xl font-bold font-display text-white hover:text-gray-300 no-underline">
        🎥 MovieMesh
        </Link>
        <SearchBar />
        <Lists />
        <div>
        {!isLoginPage && <Link to="/login">
            <button className="bg-white text-gray-900 px-4 py-2 rounded-md hover:bg-gray-200 cursor-pointer">Login</button>
        </Link>}
        </div>
      </div>
      </div>
    </nav>
  )
}

export default Navbar