import { AppBar, Box, Button, Toolbar } from "@mui/material";
import { PageSelection } from "../App";

interface HeaderProps {
  setPage: (page: PageSelection) => void;
}

const Header = (props: HeaderProps) => {
  return (
    <Box sx={{ flexGrow: 1, marginBottom: 1 }}>
      <AppBar position="static">
        <Toolbar sx={{ justifyContent: "center" }}>
          <Button color="inherit" onClick={() => props.setPage("home")}>
            Home
          </Button>
          <Button color="inherit" onClick={() => props.setPage("login")}>
            Login
          </Button>
          <Button color="inherit" onClick={() => props.setPage("register")}>
            Register
          </Button>
          <Button color="inherit" onClick={() => props.setPage("triage")}>
            Triage
          </Button>
          <Button
            color="inherit"
            onClick={() => props.setPage("email-notification")}
          >
            Notify
          </Button>
        </Toolbar>
      </AppBar>
    </Box>
  );
};

export default Header;
