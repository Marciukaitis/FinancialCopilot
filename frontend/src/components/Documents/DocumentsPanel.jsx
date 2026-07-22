import PropTypes from "prop-types";
import Box from "@mui/material/Box";
import Divider from "@mui/material/Divider";
import Typography from "@mui/material/Typography";
import KnowledgeBaseStatus from "./KnowledgeBaseStatus";
import SampleQuestions from "./SampleQuestions";

function DocumentsPanel({ status, onSelectQuestion }) {
  return (
    <Box
      sx={{
        height: "100%",
        display: "flex",
        flexDirection: "column",
        overflow: "hidden",
        borderRadius: 4,
        border: "1px solid",
        borderColor: "rgba(109,143,136,0.16)",
        background:
          "linear-gradient(165deg, rgba(251,250,248,0.96) 0%, rgba(241,240,236,0.9) 100%)",
        backdropFilter: "blur(14px)",
        boxShadow: "0 14px 40px rgba(47,55,53,0.06)",
      }}
    >
      <Box
        sx={{
          px: 2.25,
          py: 1.75,
          borderBottom: "1px solid",
          borderColor: "divider",
          background:
            "linear-gradient(120deg, rgba(196,210,218,0.28), rgba(201,221,215,0.32))",
        }}
      >
        <Typography variant="h5" sx={{ fontSize: "1.15rem" }}>
          Preguntas demo
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ fontSize: "0.82rem" }}>
          Tocá una para enviarla al chat
        </Typography>
      </Box>

      <Box
        sx={{
          flex: 1,
          minHeight: 0,
          display: "flex",
          flexDirection: "column",
          p: 2,
          gap: 1.25,
        }}
      >
        <KnowledgeBaseStatus status={status} />
        <Divider sx={{ borderColor: "rgba(109,143,136,0.12)" }} />
        <SampleQuestions onSelect={onSelectQuestion} />
      </Box>
    </Box>
  );
}

DocumentsPanel.propTypes = {
  status: PropTypes.object,
  onSelectQuestion: PropTypes.func.isRequired,
};

DocumentsPanel.defaultProps = {
  status: {},
};

export default DocumentsPanel;
