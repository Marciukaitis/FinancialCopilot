import { useRef } from "react";
import PropTypes from "prop-types";
import CloudUploadOutlinedIcon from "@mui/icons-material/CloudUploadOutlined";
import Alert from "@mui/material/Alert";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import CircularProgress from "@mui/material/CircularProgress";
import Stack from "@mui/material/Stack";
import Tooltip from "@mui/material/Tooltip";
import Typography from "@mui/material/Typography";

function UploadButton({ onUpload, uploading, error, lastUploaded }) {
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
    <Stack spacing={0.75} alignItems={{ xs: "stretch", sm: "flex-end" }}>
      <input
        ref={inputRef}
        type="file"
        accept="application/pdf,.pdf"
        hidden
        onChange={handleFileChange}
      />

      <Tooltip
        title={
          lastUploaded && !error
            ? `Último: ${lastUploaded}`
            : "Subí un PDF para indexarlo automáticamente"
        }
      >
        <span>
          <Button
            variant="contained"
            startIcon={
              uploading ? (
                <CircularProgress size={16} color="inherit" />
              ) : (
                <CloudUploadOutlinedIcon />
              )
            }
            onClick={() => inputRef.current?.click()}
            disabled={uploading}
            sx={{
              minWidth: 148,
              height: 44,
              px: 2,
              boxShadow: "0 8px 22px rgba(109,143,136,0.16)",
            }}
          >
            {uploading ? "Indexando…" : "Subir PDF"}
          </Button>
        </span>
      </Tooltip>

      {lastUploaded && !error && (
        <Typography
          variant="caption"
          color="primary.dark"
          fontWeight={600}
          sx={{
            maxWidth: 220,
            overflow: "hidden",
            textOverflow: "ellipsis",
            whiteSpace: "nowrap",
            textAlign: "right",
          }}
        >
          ✓ {lastUploaded}
        </Typography>
      )}

      {error && (
        <Alert severity="error" sx={{ py: 0, px: 1, borderRadius: 2, maxWidth: 280 }}>
          {error}
        </Alert>
      )}
    </Stack>
  );
}

UploadButton.propTypes = {
  onUpload: PropTypes.func.isRequired,
  uploading: PropTypes.bool,
  error: PropTypes.string,
  lastUploaded: PropTypes.string,
};

UploadButton.defaultProps = {
  uploading: false,
  error: "",
  lastUploaded: "",
};

export default UploadButton;
