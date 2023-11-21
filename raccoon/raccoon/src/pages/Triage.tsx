import {
  Box,
  Button,
  Checkbox,
  FormControl,
  FormControlLabel,
  FormGroup,
  InputLabel,
  MenuItem,
  Select,
  Typography,
} from "@mui/material";
import { useState } from "react";
import Cookies from "universal-cookie";

export interface TriageProps {}

type InflammationType = "none" | "moderate" | "severe";

interface FormFields {
  pain_level: number;
  head_trauma: boolean;
  allergies: boolean;
  runny_nose: boolean;
  sore_throat: boolean;
  shortness_of_breath: boolean;
  inflammation: InflammationType;
  fever: boolean;
  cough: boolean;
  chest_pain: boolean;
  breathing_difficulty: boolean;
}

const DEFAULT_FORM_STATE: FormFields = {
  pain_level: 0,
  head_trauma: false,
  allergies: false,
  runny_nose: false,
  sore_throat: false,
  shortness_of_breath: false,
  inflammation: "none",
  fever: false,
  cough: false,
  chest_pain: false,
  breathing_difficulty: false,
};

type RequestFields = FormFields & {
  username: string;
  token: string;
};

interface CheckOptionProps {
  label: string;
  field: boolean;
  handle(event: any): any;
}

const CheckOption = (props: CheckOptionProps) => {
  return (
    <FormControlLabel
      control={<Checkbox checked={props.field} onChange={props.handle} />}
      label={props.label}
    />
  );
};

interface FormViewProps {
  submitForm(form: FormFields): any;
}

const FormView = (props: FormViewProps) => {
  const [form, setForm] = useState<FormFields>(DEFAULT_FORM_STATE);
  return (
    <Box>
      <Typography>Enter your symptoms:</Typography>
      <FormGroup>
        <CheckOption
          label="Head Trauma"
          field={form.head_trauma}
          handle={(e) => setForm({ ...form, head_trauma: e.target.checked })}
        />
        <CheckOption
          label="Allergies"
          field={form.allergies}
          handle={(e) => setForm({ ...form, allergies: e.target.checked })}
        />
        <CheckOption
          label="Runny Nose"
          field={form.runny_nose}
          handle={(e) => setForm({ ...form, runny_nose: e.target.checked })}
        />
        <CheckOption
          label="Sore Throat"
          field={form.sore_throat}
          handle={(e) => setForm({ ...form, sore_throat: e.target.checked })}
        />
        <CheckOption
          label="Shortness of Breath"
          field={form.shortness_of_breath}
          handle={(e) =>
            setForm({ ...form, shortness_of_breath: e.target.checked })
          }
        />
        <CheckOption
          label="Fever"
          field={form.fever}
          handle={(e) => setForm({ ...form, fever: e.target.checked })}
        />
        <CheckOption
          label="Cough"
          field={form.cough}
          handle={(e) => setForm({ ...form, cough: e.target.checked })}
        />
        <CheckOption
          label="Chest Pain"
          field={form.chest_pain}
          handle={(e) => setForm({ ...form, chest_pain: e.target.checked })}
        />
        <CheckOption
          label="Difficulty Breathing"
          field={form.breathing_difficulty}
          handle={(e) =>
            setForm({ ...form, breathing_difficulty: e.target.checked })
          }
        />
        <Box paddingY={1} />
        <FormControl>
          <InputLabel id="pain-input-label">Pain Level</InputLabel>
          <Select
            labelId="pain-input-label"
            label="Pain Level"
            onChange={(e) =>
              setForm({ ...form, pain_level: e.target.value as number })
            }
            defaultValue={1}
          >
            <MenuItem value={1}>1</MenuItem>
            <MenuItem value={2}>2</MenuItem>
            <MenuItem value={3}>3</MenuItem>
            <MenuItem value={4}>4</MenuItem>
            <MenuItem value={5}>5</MenuItem>
            <MenuItem value={6}>6</MenuItem>
            <MenuItem value={7}>7</MenuItem>
            <MenuItem value={8}>8</MenuItem>
            <MenuItem value={9}>9</MenuItem>
          </Select>
        </FormControl>
        <Box paddingY={1} />
        <FormControl>
          <InputLabel id="inflammation-input-label">
            Inflamation Level
          </InputLabel>
          <Select
            labelId="inflammation-input-label"
            label="Inflamation Level"
            onChange={(e) =>
              setForm({
                ...form,
                inflammation: e.target.value as InflammationType,
              })
            }
            defaultValue={"none"}
          >
            <MenuItem value="none">None</MenuItem>
            <MenuItem value="moderate">Moderate</MenuItem>
            <MenuItem value="severe">Severe</MenuItem>
          </Select>
        </FormControl>
      </FormGroup>
      <Button onClick={() => props.submitForm(form)}>Submit</Button>
    </Box>
  );
};

const Triage = (props: TriageProps) => {
  const cookies = new Cookies();
  const [view, setView] = useState<"form" | "results">("form");

  const submitForm = async (form: FormFields) => {
    const username = cookies.get("username");
    const token = cookies.get("login-token");

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

    const data = await response.json();
    console.log(data);
  };

  return (
    <Box padding={10}>
      <FormView submitForm={submitForm} />
    </Box>
  );
};

export default Triage;
