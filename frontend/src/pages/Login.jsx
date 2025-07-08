import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const navigate = useNavigate();
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    const res = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    if (!res.ok) {
      setError("Invalid credentials");
      return;
    }

    const { access_token, token_type } = await res.json();
    localStorage.setItem("token", access_token);
    navigate("/");
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col items-center justify-center mt-36">
      <h1 className="text-2xl font-bold mb-4">Login to MovieMesh</h1>
      <input value={username} onChange={e => setUsername(e.target.value)} placeholder="Username" className="w-1/3 p-3 border-2 border-gray-300 rounded-md focus:border-blue-500 m-1" />
      <input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="Password" className="w-1/3 p-3 border-2 border-gray-300 rounded-md focus:border-blue-500 m-1" />
      <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 cursor-pointer m-4">Login</button>
      {error && <div className="text-red-600">{error}</div>}
    </form>
  );
}

export default Login;