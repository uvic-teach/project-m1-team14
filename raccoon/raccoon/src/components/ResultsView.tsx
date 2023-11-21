import { Box, Typography } from "@mui/material";

export interface Results {
  cause: string;
  medicine: string;
  result: string;
}

interface ResultsViewProps {
  results: Results;
}

const ResultsView = (props: ResultsViewProps) => {
  return (
    <Box>
      <Typography>Cause: {props.results.cause}</Typography>
      <Typography>Medicine: {props.results.medicine}</Typography>
      <Typography>Result: {props.results.result}</Typography>
    </Box>
  );
};

export default ResultsView;
