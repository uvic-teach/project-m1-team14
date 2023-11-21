import { Box, Button, TextField, Typography } from "@mui/material";
import { useState } from "react";
import Cookies from "universal-cookie";

interface NotifyProps {}

const Notify = (props: NotifyProps) => {
  const [email, setEmail] = useState<string>("");
  const [view, setView] = useState<"enter" | "success" | "failure">("enter");
  const cookies = new Cookies();
  const username = cookies.get("username");
  const token = cookies.get("login-token", {
    doNotParse: true,
  });

  const registerEmail = async () => {
    const response = await fetch("https://seng350.kjs.dev/register", {
      method: "POST",
      cache: "no-cache",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        token,
        username,
        email,
      }),
    });

    if (response.ok) {
    }
  };

  return (
    <Box padding={1}>
      {view === "enter" && (
        <>
          <Typography>Notify me when an ER spot is open</Typography>
          <TextField
            onChange={(e) => setEmail(e.target.value)}
            placeholder="address@email.com"
          />
          <Button onClick={registerEmail}>Register</Button>
        </>
      )}
      {view === "failure" && (
        <>
          <Typography>Failed to register your email.</Typography>
          <Button onClick={() => setView("enter")}>Try again</Button>
        </>
      )}
      {view === "success" && (
        <>
          <Typography>Email registered successfully!</Typography>
          <Button onClick={() => setView("enter")}>Register another</Button>
        </>
      )}
    </Box>
  );
};

export default Notify;
