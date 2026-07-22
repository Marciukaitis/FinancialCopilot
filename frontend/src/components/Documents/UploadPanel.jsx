import { useRef } from "react";
import PropTypes from "prop-types";
import CloudUploadOutlinedIcon from "@mui/icons-material/CloudUploadOutlined";
import Alert from "@mui/material/Alert";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";

function UploadPanel({ onUpload, uploading, error, lastUploaded }) {
  const inputRef = useRef(null);

  const handleFileChange = async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;

    try {
      await onUpload(file);
    } finally {
      event.target.value = "";
    }
  };

  return (
    <Box>
      <Typography variant="subtitle2" sx={{ mb: 1.5, color: "text.secondary" }}>
        Subir PDF
      </Typography>

      <Stack
        spacing={1.5}
        sx={{
          p: 2,
          borderRadius: 2,
          border: "1px dashed",
          borderColor: "divider",
          bgcolor: "background.default",
        }}
      >
        <Typography variant="body2" color="text.secondary">
          Seleccioná un documento financiero. Se indexará automáticamente.
        </Typography>

        <input
          ref={inputRef}
          type="file"
          accept="application/pdf,.pdf"
          hidden
          onChange={handleFileChange}
        />

        <Button
          variant="outlined"
          startIcon={<CloudUploadOutlinedIcon />}
          onClick={() => inputRef.current?.click()}
          disabled={uploading}
        >
          {uploading ? "Subiendo e indexando…" : "Elegir PDF"}
        </Button>

        {lastUploaded && !error && (
          <Typography variant="caption" color="text.secondary">
            Último archivo: {lastUploaded}
          </Typography>
        )}

        {error && (
          <Alert severity="error" sx={{ py: 0 }}>
            {error}
          </Alert>
        )}
      </Stack>
    </Box>
  );
}

UploadPanel.propTypes = {
  onUpload: PropTypes.func.isRequired,
  uploading: PropTypes.bool,
  error: PropTypes.string,
  lastUploaded: PropTypes.string,
};

UploadPanel.defaultProps = {
  uploading: false,
  error: "",
  lastUploaded: "",
};

export default UploadPanel;
