import { createTheme } from "@mui/material/styles";

const theme = createTheme({
  palette: {
    mode: "light",
    primary: {
      main: "#1f4b3f",
      light: "#3d6f61",
      dark: "#12332b",
      contrastText: "#ffffff",
    },
    secondary: {
      main: "#c4a574",
    },
    background: {
      default: "#f3f1ec",
      paper: "#ffffff",
    },
    text: {
      primary: "#1c1c1c",
      secondary: "#5f6360",
    },
    divider: "#e4e0d8",
  },
  typography: {
    fontFamily: '"IBM Plex Sans", "Helvetica Neue", Arial, sans-serif',
    h1: {
      fontFamily: '"IBM Plex Serif", Georgia, serif',
      fontWeight: 600,
    },
    h2: {
      fontFamily: '"IBM Plex Serif", Georgia, serif',
      fontWeight: 600,
    },
    h5: {
      fontFamily: '"IBM Plex Serif", Georgia, serif',
      fontWeight: 600,
    },
    button: {
      textTransform: "none",
      fontWeight: 600,
    },
  },
  shape: {
    borderRadius: 10,
  },
  components: {
    MuiButton: {
      defaultProps: {
        disableElevation: true,
      },
    },
    MuiPaper: {
      defaultProps: {
        elevation: 0,
      },
      styleOverrides: {
        root: {
          backgroundImage: "none",
        },
      },
    },
  },
});

export default theme;
