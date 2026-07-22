import PropTypes from "prop-types";
import Box from "@mui/material/Box";
import Divider from "@mui/material/Divider";
import Paper from "@mui/material/Paper";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import IndexStatus from "./IndexStatus";
import UploadPanel from "./UploadPanel";

function DocumentsPanel({
  status,
  uploading,
  error,
  lastUploaded,
  onUpload,
}) {
  return (
    <Paper
      sx={{
        height: "100%",
        border: "1px solid",
        borderColor: "divider",
        p: 2.5,
        display: "flex",
        flexDirection: "column",
        gap: 2.5,
      }}
    >
      <Box>
        <Typography variant="h5">Documentos</Typography>
        <Typography variant="body2" color="text.secondary">
          Gestión e índice vectorial
        </Typography>
      </Box>

      <Divider />

      <IndexStatus status={status} />

      <Divider />

      <UploadPanel
        onUpload={onUpload}
        uploading={uploading}
        error={error}
        lastUploaded={lastUploaded}
      />

      <Stack sx={{ mt: "auto" }} spacing={0.5}>
        <Typography variant="caption" color="text.secondary">
          Colección: {status?.collection_name || "finance_documents"}
        </Typography>
      </Stack>
    </Paper>
  );
}

DocumentsPanel.propTypes = {
  status: PropTypes.object,
  uploading: PropTypes.bool,
  error: PropTypes.string,
  lastUploaded: PropTypes.string,
  onUpload: PropTypes.func.isRequired,
};

DocumentsPanel.defaultProps = {
  status: {},
  uploading: false,
  error: "",
  lastUploaded: "",
};

export default DocumentsPanel;
