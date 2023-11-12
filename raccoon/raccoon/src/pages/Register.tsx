import { Box, Button, TextField, Typography } from "@mui/material";
import { useState } from "react";
import Cookies from "universal-cookie";

interface RegisterProps {}

const Register = (props: RegisterProps) => {
  const [username, setUsername] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const cookies = new Cookies();

  const attemptRegistration = async (user: string, pass: string) => {
    // TODO: implement API call and set cookie
    const body = {
      username: user,
      password: pass,
    };
    const response = await fetch(
      "https://fr1gi6xdtc.execute-api.us-west-2.amazonaws.com/prod/register",
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
    } else if (response.status === 400) {
    } else {
      // error
    }
  };

  return (
    <Box>
      <Typography>Create an Account</Typography>
      <TextField
        onChange={(e) => setUsername(e.target.value)}
        placeholder="Username"
      />
      <TextField
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
        type="password"
      />
      <Button onClick={() => attemptRegistration(username, password)}>
        SUBMIT
      </Button>
    </Box>
  );
};

export default Register;
