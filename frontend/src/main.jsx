import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import App from "./App";
import Search from "./pages/Search";
import Movie from "./pages/Movie";
import Login from "./pages/Login";
import Home from "./pages/Home";
import Profile from "./pages/Profile";
import Register from "./pages/Register";
import Actors from "./pages/Actors";
import Directors from "./pages/Directors";
import Movies from "./pages/Movies";
import Actor from "./pages/Actor";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <BrowserRouter>
    <Routes>
      <Route element={<App />}>
        <Route path="/" element={<Home />} />
        <Route path="/search" element={<Search />} />
        <Route path="/movie/:id" element={<Movie />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/lists/actors" element={<Actors />} />
        <Route path="/lists/directors" element={<Directors />} />
        <Route path="/lists/movies" element={<Movies />} />
        <Route path="/profile/:id" element={<Profile />} />
        <Route path="/actors/:id" element={<Actor />} />
      </Route>
    </Routes>
  </BrowserRouter>
);
