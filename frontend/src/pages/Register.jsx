import { useState, useContext } from "react";
import { useNavigate, Link } from "react-router-dom";
import { SearchContext } from "../components/SearchContext";

function Register() {
  const [username, setUsername] = useState("");
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  // Access global auth setters
  const { setIsLoggedIn, setUser } = useContext(SearchContext);

  const navigate = useNavigate();
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    const res = await fetch("/api/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password, name }),
    });

    if (!res.ok) {
      if (res.status === 400) {
        setError("Username already taken");
      } else if (res.status === 422) {
        setError("Invalid credentials");
      } else {
        setError("Registration failed");
      }
      return;
    }

    // Log the user in right after successful registration
    const loginRes = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    if (!loginRes.ok) {
      setError("Login failed after registration");
      return;
    }

    const { access_token } = await loginRes.json();

    localStorage.setItem("token", access_token);

    // Fetch user info so navbar/profile reflect login immediately
    try {
      const uRes = await fetch("/api/me", {
        headers: { Authorization: `Bearer ${access_token}` },
      });
      if (uRes.ok) {
        const uData = await uRes.json();
        setUser(uData);
      }
    } catch (err) {
      console.error("Failed to fetch user after login", err);
    }

    setIsLoggedIn(true);
    navigate("/");
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col items-center justify-center mt-36">
      <h1 className="text-2xl font-bold mb-4">Register for MovieMesh</h1>
      <input value={username} onChange={e => setUsername(e.target.value)} placeholder="Username" className="w-1/3 p-3 border-2 border-gray-300 rounded-md focus:border-blue-500 m-1" />
      <input value={name} onChange={e => setName(e.target.value)} placeholder="Name" className="w-1/3 p-3 border-2 border-gray-300 rounded-md focus:border-blue-500 m-1" />
      <input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="Password" className="w-1/3 p-3 border-2 border-gray-300 rounded-md focus:border-blue-500 m-1" />
      <div className="flex justify-between">
        <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 cursor-pointer m-4">Register</button>
        <Link to="/login"><button className="border-2 border-blue-700 text-blue-700 px-2 py-2 rounded-md hover:bg-blue-700 hover:text-white cursor-pointer m-4">Login</button></Link>
      </div>
      {error && <div className="text-red-600">{error}</div>}
    </form>
  );
}

export default Register;