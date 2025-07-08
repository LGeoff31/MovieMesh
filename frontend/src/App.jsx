import { Outlet, Link } from 'react-router-dom';
import Navbar from './components/Navbar';
import { useState, useEffect } from 'react';
import { SearchContext } from './components/SearchContext';

export default function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState(null);
  const [searchResults, setSearchResults] = useState([]);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) return;

    const fetchUser = async () => {
      const res = await fetch("/api/me", {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (res.ok) {
        const data = await res.json();
        setUser(data);
        setIsLoggedIn(true);
        console.log(data);
      }
    };

    fetchUser();
  }, []);

  return (
    <>
      <SearchContext.Provider value={{searchResults, setSearchResults, user, setUser, isLoggedIn, setIsLoggedIn}}>
        <Navbar />
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 min-h-1/2">
          <Outlet />
        </div>
      </SearchContext.Provider>
    </>
  );
}
