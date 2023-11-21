import { Box, Button } from "@mui/material";
import { useState } from "react";
import Cookies from "universal-cookie";
import FormView, { FormFields } from "../components/FormView";
import ResultsView, { Results } from "../components/ResultsView";

export interface TriageProps {}

type RequestFields = FormFields & {
  username: string;
  token: string;
};

const Triage = (props: TriageProps) => {
  const cookies = new Cookies();
  const [results, setResults] = useState<Results | undefined>();

  const submitForm = async (form: FormFields) => {
    const username = cookies.get("username");
    const token: string = cookies.get("login-token", {
      doNotParse: true,
    });

    const body: RequestFields = {
      ...form,
      username,
      token,
    };

    const response = await fetch("https://triage-ms.azurewebsites.net/triage", {
      method: "POST",
      cache: "no-cache",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });

    if (response.ok) {
      const data = await response.json();
      setResults(data as Results);
    } else {
    }
  };

  return (
    <Box paddingY={1} paddingX={10}>
      {results === undefined ? (
        <FormView submitForm={submitForm} />
      ) : (
        <>
          <ResultsView results={results} />
          <Button onClick={() => setResults(undefined)}>Retry</Button>
        </>
      )}
    </Box>
  );
};

export default Triage;
