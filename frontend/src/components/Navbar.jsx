import { Link, useNavigate } from "react-router-dom";
import SearchBar from "./SearchBar";
import Lists from "./Lists";
import { useContext } from "react";
import { SearchContext } from "./SearchContext";

const Navbar = () => {
  const { isLoggedIn, user, setIsLoggedIn, setUser } = useContext(SearchContext);

  const navigate = useNavigate();

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
          {!isLoggedIn && <Link to="/login">
            <button className="bg-white text-gray-900 px-4 py-2 rounded-md hover:bg-gray-200 cursor-pointer">Login</button>
          </Link>}
          {isLoggedIn && 
          <div className="flex items-center gap-4">
            <button
              className="bg-white text-gray-900 px-4 py-2 rounded-md hover:bg-gray-200 cursor-pointer"
              onClick={() => {
                localStorage.removeItem("token");
                setIsLoggedIn(false);
                setUser(null);
                navigate("/");
              }}
            >
              Logout
            </button>
            <Link to={`/profile/${user.user_id}`}>
              <img src={"/profile.jpg"} alt="Profile" className="w-10 h-10 rounded-full cursor-pointer hover:scale-110 transition-all duration-300" />
            </Link>
          </div>}
        </div>
      </div>
      </div>
    </nav>
  )
}

export default Navbar