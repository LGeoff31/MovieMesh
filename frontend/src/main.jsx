import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import App from "./App";
import Search from "./pages/Search";
import Movie from "./pages/Movie";
import Login from "./pages/Login";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <BrowserRouter>
    <Routes>
      <Route element={<App />}>
        <Route path="/" element={<Search />} />
        <Route path="/search" element={<Search />} />
        <Route path="/movie/:id" element={<Movie />} />
        <Route path="/login" element={<Login />} />
      </Route>
    </Routes>
  </BrowserRouter>
);
