import { useEffect, useState } from "react";
import PropTypes from "prop-types";
import Box from "@mui/material/Box";
import CircularProgress from "@mui/material/CircularProgress";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";

const STEPS = [
  { id: "search", label: "Searching documents" },
  { id: "retrieve", label: "Retrieving chunks" },
  { id: "generate", label: "Generating answer" },
  { id: "validate", label: "Validating response" },
];

const STEP_DURATION_MS = 1000;

function RagPipeline({ loading }) {
  const [stepIndex, setStepIndex] = useState(0);

  useEffect(() => {
    if (!loading) {
      setStepIndex(0);
      return undefined;
    }

    setStepIndex(0);

    const timers = STEPS.slice(0, -1).map((_, index) =>
      window.setTimeout(() => {
        setStepIndex(index + 1);
      }, (index + 1) * STEP_DURATION_MS),
    );

    return () => timers.forEach((timer) => window.clearTimeout(timer));
  }, [loading]);

  if (!loading) return null;

  const step = STEPS[stepIndex];

  return (
    <Box
      className="fc-message-in"
      sx={{
        maxWidth: { xs: "92%", md: "78%" },
        mb: 1.75,
        px: 2.1,
        py: 1.7,
        borderRadius: "18px 18px 18px 6px",
        background: "rgba(255,255,255,0.95)",
        border: "1px solid rgba(15,118,110,0.12)",
        boxShadow: "0 8px 20px rgba(11,31,28,0.05)",
      }}
    >
      <Stack direction="row" spacing={1} alignItems="center" sx={{ mb: 1.1 }}>
        <CircularProgress size={14} thickness={5} />
        <Typography
          variant="caption"
          sx={{
            fontWeight: 700,
            letterSpacing: 0.6,
            textTransform: "uppercase",
            color: "text.secondary",
          }}
        >
          Thinking…
        </Typography>
      </Stack>

      <Stack
        key={step.id}
        direction="row"
        spacing={1}
        alignItems="center"
        className="fc-message-in"
      >
        <CircularProgress size={14} thickness={5} sx={{ m: "2px" }} />
        <Typography variant="body2" sx={{ fontWeight: 600, color: "text.primary" }}>
          {step.label}
        </Typography>
      </Stack>
    </Box>
  );
}

RagPipeline.propTypes = {
  loading: PropTypes.bool,
};

RagPipeline.defaultProps = {
  loading: false,
};

export default RagPipeline;
