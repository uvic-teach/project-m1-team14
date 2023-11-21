import React, { useState } from "react";
import "./App.css";
import Header from "./components/Header";
import { Typography } from "@mui/material";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Triage from "./pages/Triage";
import Notify from "./pages/Notify";

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
    <div className="App">
      <Header setPage={setPage} />
      {page === "home" && <Typography>Welcome home</Typography>}
      {page === "login" && <Login />}
      {page === "register" && <Register />}
      {page === "triage" && <Triage />}
      {page === "email-notification" && <Notify />}
    </div>
  );
}

export default App;
