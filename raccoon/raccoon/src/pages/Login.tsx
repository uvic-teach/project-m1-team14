import { Box, Button, TextField, Typography } from "@mui/material";
import { useState } from "react";
import Cookies from "universal-cookie";

interface LoginProps {}

const Login = (props: LoginProps) => {
  const [username, setUsername] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [view, setView] = useState<"enter" | "success" | "failure">("enter");
  const cookies = new Cookies();

  async function sha256(message: string) {
    // encode as UTF-8
    const msgBuffer = new TextEncoder().encode(message);

    // hash the message
    const hashBuffer = await crypto.subtle.digest("SHA-256", msgBuffer);

    // convert ArrayBuffer to Array
    const hashArray = Array.from(new Uint8Array(hashBuffer));

    // convert bytes to hex string
    const hashHex = hashArray
      .map((b) => b.toString(16).padStart(2, "0"))
      .join("");
    return hashHex.toLowerCase();
  }

  const attemptLogin = async (user: string, pass: string) => {
    const hash = await sha256(pass);
    const body = {
      username: user,
      password: hash,
    };
    const response = await fetch(
      "https://fr1gi6xdtc.execute-api.us-west-2.amazonaws.com/prod/login",
      {
        method: "POST",
        cache: "no-cache",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      }
    );

    if (response.status === 200) {
      const res = await response.json();
      cookies.set("login-token", res.token, {
        path: "/",
        expires: new Date(res.expiration * 1000),
        sameSite: "lax",
      });
      cookies.set("username", user, {
        path: "/",
        expires: new Date(res.expiration * 1000),
        sameSite: "lax",
      });
      setView("success");
    } else if (response.status === 400) {
      console.log(response);
      setView("failure");
    } else {
      // error
      console.log(response);
      setView("failure");
    }
  };

  return (
    <>
      {view === "enter" && (
        <Box>
          <Typography>Log In</Typography>
          <TextField
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Username"
          />
          <TextField
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
            type="password"
          />
          <Button onClick={() => attemptLogin(username, password)}>
            SUBMIT
          </Button>
        </Box>
      )}
      {view === "failure" && (
        <Box>
          <Typography>Could not log you in.</Typography>
          <Button onClick={() => setView("enter")}>Try again</Button>
        </Box>
      )}
      {view === "success" && (
        <Box>
          <Typography>
            You are now signed in! Try going to the "Triage" page and submitting
            the form!
          </Typography>
        </Box>
      )}
    </>
  );
};

export default Login;
