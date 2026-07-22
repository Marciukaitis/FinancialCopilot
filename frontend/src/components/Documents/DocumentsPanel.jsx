import PropTypes from "prop-types";
import Box from "@mui/material/Box";
import Divider from "@mui/material/Divider";
import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";
import KnowledgeBaseStatus from "./KnowledgeBaseStatus";
import SampleQuestions from "./SampleQuestions";
import UploadPanel from "./UploadPanel";

function DocumentsPanel({
  status,
  uploading,
  error,
  lastUploaded,
  onUpload,
  onSelectQuestion,
}) {
  return (
    <Paper
      sx={{
        height: "100%",
        border: "1px solid",
        borderColor: "divider",
        display: "flex",
        flexDirection: "column",
        overflow: "hidden",
      }}
    >
      <Box sx={{ px: 2.5, py: 2, borderBottom: "1px solid", borderColor: "divider" }}>
        <Typography variant="h5">Knowledge Base</Typography>
        <Typography variant="body2" color="text.secondary">
          Documentos, estado del índice y preguntas de demo
        </Typography>
      </Box>

      <Box sx={{ flex: 1, overflowY: "auto", p: 2.5 }}>
        <KnowledgeBaseStatus status={status} />

        <Divider sx={{ my: 2.5 }} />

        <UploadPanel
          onUpload={onUpload}
          uploading={uploading}
          error={error}
          lastUploaded={lastUploaded}
        />

        <Divider sx={{ my: 2.5 }} />

        <SampleQuestions onSelect={onSelectQuestion} />
      </Box>
    </Paper>
  );
}

DocumentsPanel.propTypes = {
  status: PropTypes.object,
  uploading: PropTypes.bool,
  error: PropTypes.string,
  lastUploaded: PropTypes.string,
  onUpload: PropTypes.func.isRequired,
  onSelectQuestion: PropTypes.func.isRequired,
};

DocumentsPanel.defaultProps = {
  status: {},
  uploading: false,
  error: "",
  lastUploaded: "",
};

export default DocumentsPanel;
