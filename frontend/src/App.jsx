import { Outlet, Link } from 'react-router-dom';

export default function App() {
  return (
    <>
      <nav className="bg-gray-900 text-white mb-4">
        <div className="w-full mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center h-16">
            <Link to="/" className="text-xl font-bold text-white hover:text-gray-300 no-underline">
              IMDB-Clone
            </Link>
          </div>
        </div>
      </nav>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <Outlet />
      </div>
    </>
  );
}
