import { Outlet, Link } from 'react-router-dom';
import Navbar from './components/Navbar';
import { useState } from 'react';
import { SearchContext } from './components/SearchContext';

export default function App() {
  
  const [searchResults, setSearchResults] = useState([]);

  return (
    <>
      <SearchContext.Provider value={{searchResults, setSearchResults}}>
        <Navbar />
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 min-h-1/2">
          <Outlet />
        </div>
      </SearchContext.Provider>
    </>
  );
}
