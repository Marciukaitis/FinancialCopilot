import PropTypes from "prop-types";
import CheckCircleOutlineIcon from "@mui/icons-material/CheckCircleOutline";
import Box from "@mui/material/Box";
import Chip from "@mui/material/Chip";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";

function KnowledgeBaseStatus({ status }) {
  const documents = status?.documents?.length
    ? status.documents
    : [];
  const indexed = Boolean(status?.indexed);

  return (
    <Box>
      <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 1.5 }}>
        <Typography variant="subtitle2" color="text.secondary">
          Knowledge Base
        </Typography>
        <Chip
          size="small"
          label={indexed ? "Indexado" : "Pendiente"}
          color={indexed ? "success" : "default"}
          variant={indexed ? "filled" : "outlined"}
        />
      </Stack>

      <Stack spacing={1}>
        {documents.length === 0 ? (
          <Typography variant="body2" color="text.secondary">
            Todavía no hay PDFs cargados.
          </Typography>
        ) : (
          documents.map((name) => (
            <Stack key={name} direction="row" spacing={1} alignItems="center">
              <CheckCircleOutlineIcon fontSize="small" color="success" />
              <Typography variant="body2">{name}</Typography>
            </Stack>
          ))
        )}
      </Stack>

      <Stack
        spacing={0.75}
        sx={{
          mt: 2,
          p: 1.5,
          borderRadius: 2,
          bgcolor: "background.default",
          border: "1px solid",
          borderColor: "divider",
        }}
      >
        <Typography variant="body2">
          Chunks: <strong>{status?.chunks_indexed ?? 0}</strong>
        </Typography>
        <Typography variant="body2">
          Embeddings: <strong>{status?.embedding_model || "HuggingFace"}</strong>
        </Typography>
        <Typography variant="body2">
          Vector DB: <strong>{status?.vector_db || "ChromaDB"}</strong>
        </Typography>
        <Typography variant="body2">
          LLM: <strong>{status?.llm_model || "llama3.2"}</strong>
        </Typography>
      </Stack>
    </Box>
  );
}

KnowledgeBaseStatus.propTypes = {
  status: PropTypes.shape({
    documents: PropTypes.arrayOf(PropTypes.string),
    chunks_indexed: PropTypes.number,
    embedding_model: PropTypes.string,
    llm_model: PropTypes.string,
    vector_db: PropTypes.string,
    indexed: PropTypes.bool,
  }),
};

KnowledgeBaseStatus.defaultProps = {
  status: {},
};

export default KnowledgeBaseStatus;
