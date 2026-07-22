import PropTypes from "prop-types";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Chip from "@mui/material/Chip";
import Divider from "@mui/material/Divider";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import {
  FOLLOWUP_FLOW,
  OUT_OF_SCOPE_QUESTIONS,
  SAMPLE_QUESTIONS,
} from "../../data/sampleQuestions";

function QuestionButton({ question, onSelect, tone }) {
  return (
    <Button
      fullWidth
      variant="text"
      onClick={() => onSelect(question)}
      sx={{
        justifyContent: "flex-start",
        textAlign: "left",
        color: tone === "warning" ? "text.secondary" : "text.primary",
        fontWeight: 400,
        px: 1,
        py: 0.75,
        borderRadius: 1.5,
        bgcolor: tone === "warning" ? "rgba(0,0,0,0.02)" : "transparent",
        "&:hover": {
          bgcolor: "rgba(31,75,63,0.06)",
        },
      }}
    >
      {question}
    </Button>
  );
}

QuestionButton.propTypes = {
  question: PropTypes.string.isRequired,
  onSelect: PropTypes.func.isRequired,
  tone: PropTypes.oneOf(["default", "warning"]),
};

QuestionButton.defaultProps = {
  tone: "default",
};

function SampleQuestions({ onSelect }) {
  return (
    <Box>
      <Typography variant="subtitle2" color="text.secondary" sx={{ mb: 1.5 }}>
        Preguntas disponibles
      </Typography>

      <Stack spacing={2}>
        {Object.values(SAMPLE_QUESTIONS).map((group) => (
          <Box key={group.title}>
            <Typography variant="body2" fontWeight={600} sx={{ mb: 0.5 }}>
              {group.title}
            </Typography>
            <Stack spacing={0.25}>
              {group.questions.map((question) => (
                <QuestionButton
                  key={question}
                  question={question}
                  onSelect={onSelect}
                />
              ))}
            </Stack>
          </Box>
        ))}

        <Divider />

        <Box>
          <Stack direction="row" spacing={1} alignItems="center" sx={{ mb: 1 }}>
            <Typography variant="body2" fontWeight={600}>
              Preguntas de seguimiento
            </Typography>
            <Chip size="small" label="Memoria" variant="outlined" />
          </Stack>
          <Typography variant="caption" color="text.secondary" sx={{ display: "block", mb: 1 }}>
            Usá la misma sesión para demostrar LangGraph Memory.
          </Typography>
          <Stack spacing={0.25}>
            {FOLLOWUP_FLOW.map((question, index) => (
              <Stack key={question} direction="row" spacing={1} alignItems="center">
                <Typography variant="caption" color="text.secondary" sx={{ minWidth: 14 }}>
                  {index + 1}.
                </Typography>
                <QuestionButton question={question} onSelect={onSelect} />
              </Stack>
            ))}
          </Stack>
        </Box>

        <Divider />

        <Box>
          <Stack direction="row" spacing={1} alignItems="center" sx={{ mb: 1 }}>
            <Typography variant="body2" fontWeight={600}>
              Preguntas que NO debería responder
            </Typography>
            <Chip size="small" label="Anti-alucinación" color="warning" variant="outlined" />
          </Stack>
          <Typography variant="caption" color="text.secondary" sx={{ display: "block", mb: 1 }}>
            Si no está en los documentos, debe indicar que no tiene información suficiente.
          </Typography>
          <Stack spacing={0.25}>
            {OUT_OF_SCOPE_QUESTIONS.map((question) => (
              <QuestionButton
                key={question}
                question={question}
                onSelect={onSelect}
                tone="warning"
              />
            ))}
          </Stack>
        </Box>
      </Stack>
    </Box>
  );
}

SampleQuestions.propTypes = {
  onSelect: PropTypes.func.isRequired,
};

export default SampleQuestions;
