import React, { useState } from "react";
import "./App.css";
import Header from "./components/Header";
import { Typography } from "@mui/material";
import Login from "./pages/Login";
import Register from "./pages/Register";
import { CookiesProvider } from "react-cookie";

export type PageSelection =
  | "login"
  | "register"
  | "landing"
  | "triage"
  | "confirmation"
  | "er-booking"
  | "email-notification"
  | "home";

function App() {
  const [page, setPage] = useState<PageSelection>("home");

  return (
    <CookiesProvider defaultSetOptions={{ path: "/" }}>
      <div className="App">
        <Header setPage={setPage} />
        {page === "home" && <Typography>Welcome home</Typography>}
        {page === "login" && <Login />}
        {page === "register" && <Register />}
      </div>
    </CookiesProvider>
  );
}

export default App;
