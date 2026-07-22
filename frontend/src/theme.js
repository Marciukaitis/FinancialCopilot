import { createTheme } from "@mui/material/styles";

const theme = createTheme({
  palette: {
    mode: "light",
    primary: {
      main: "#6d8f88",
      light: "#9bb5af",
      dark: "#55756f",
      contrastText: "#ffffff",
    },
    secondary: {
      main: "#8aa0ad",
      contrastText: "#1f2a30",
    },
    success: {
      main: "#7d9e8f",
    },
    warning: {
      main: "#c4a484",
    },
    background: {
      default: "#f3f2ef",
      paper: "#fbfaf8",
    },
    text: {
      primary: "#2f3735",
      secondary: "#6d7774",
    },
    divider: "rgba(109, 143, 136, 0.16)",
  },
  typography: {
    fontFamily: '"DM Sans", "Helvetica Neue", sans-serif',
    h1: {
      fontFamily: '"Syne", sans-serif',
      fontWeight: 800,
      letterSpacing: "-0.04em",
    },
    h2: {
      fontFamily: '"Syne", sans-serif',
      fontWeight: 700,
      letterSpacing: "-0.03em",
    },
    h5: {
      fontFamily: '"Syne", sans-serif',
      fontWeight: 700,
      letterSpacing: "-0.02em",
    },
    h6: {
      fontFamily: '"Syne", sans-serif',
      fontWeight: 700,
      letterSpacing: "-0.02em",
    },
    button: {
      textTransform: "none",
      fontWeight: 650,
      letterSpacing: "0.01em",
    },
  },
  shape: {
    borderRadius: 16,
  },
  components: {
    MuiButton: {
      defaultProps: {
        disableElevation: true,
      },
      styleOverrides: {
        root: {
          borderRadius: 12,
        },
        containedPrimary: {
          backgroundImage: "linear-gradient(135deg, #7d9e97 0%, #6d8f88 100%)",
          "&:hover": {
            backgroundImage: "linear-gradient(135deg, #6d8f88 0%, #55756f 100%)",
          },
        },
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
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          scrollbarWidth: "thin",
          scrollbarColor: "#c5d0cc transparent",
        },
      },
    },
  },
});

export default theme;
