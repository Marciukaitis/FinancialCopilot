import { useState } from "react";
import PropTypes from "prop-types";
import VisibilityOffOutlinedIcon from "@mui/icons-material/VisibilityOffOutlined";
import VisibilityOutlinedIcon from "@mui/icons-material/VisibilityOutlined";
import Box from "@mui/material/Box";
import IconButton from "@mui/material/IconButton";
import Stack from "@mui/material/Stack";
import Tooltip from "@mui/material/Tooltip";
import Typography from "@mui/material/Typography";

function formatScore(score) {
  if (score == null || Number.isNaN(Number(score))) return "n/a";
  return Number(score).toFixed(2);
}

function cleanDocumentName(name) {
  if (!name) return "";
  const base = String(name).split(/[/\\]/).pop();
  const match = base.match(/^[0-9a-f]{32}_(.+)$/i);
  return match ? match[1] : base;
}

function pickBestChunk(chunks) {
  if (!chunks?.length) return null;

  return chunks.reduce((best, chunk) => {
    const bestScore = Number(best?.score);
    const chunkScore = Number(chunk?.score);

    if (Number.isNaN(chunkScore)) return best;
    if (Number.isNaN(bestScore)) return chunk;
    return chunkScore > bestScore ? chunk : best;
  }, chunks[0]);
}

function RetrievedContext({ chunks }) {
  const [revealed, setRevealed] = useState(false);
  const chunk = pickBestChunk(chunks);

  if (!chunk) return null;

  const documentName = cleanDocumentName(chunk.source);

  return (
    <Box sx={{ mt: 1.75 }}>
      <Typography
        variant="caption"
        sx={{
          display: "block",
          mb: 1,
          fontWeight: 700,
          letterSpacing: 0.55,
          textTransform: "uppercase",
          color: "text.secondary",
          fontSize: 10,
        }}
      >
        Retrieved Context
      </Typography>

      <Box
        sx={{
          px: 1.5,
          py: 1.15,
          borderRadius: 2.5,
          bgcolor: "rgba(15,118,110,0.04)",
          border: "1px solid rgba(15,118,110,0.12)",
        }}
      >
        <Stack direction="row" alignItems="center" spacing={0.5}>
          <Typography
            variant="body2"
            sx={{
              flex: 1,
              minWidth: 0,
              fontWeight: 600,
              overflow: "hidden",
              textOverflow: "ellipsis",
              whiteSpace: "nowrap",
            }}
            title={documentName}
          >
            {documentName}
            {chunk.metadata?.page != null ? ` · p. ${chunk.metadata.page}` : ""}
          </Typography>

          <Tooltip title={revealed ? "Ocultar score" : "Ver score"}>
            <IconButton
              size="small"
              aria-label={revealed ? "Ocultar score" : "Ver score"}
              onClick={() => setRevealed((prev) => !prev)}
              sx={{ color: "primary.dark" }}
            >
              {revealed ? (
                <VisibilityOffOutlinedIcon sx={{ fontSize: 18 }} />
              ) : (
                <VisibilityOutlinedIcon sx={{ fontSize: 18 }} />
              )}
            </IconButton>
          </Tooltip>
        </Stack>

        {revealed && (
          <Box className="fc-message-in" sx={{ mt: 0.85 }}>
            <Typography
              variant="caption"
              sx={{
                display: "inline-block",
                px: 1,
                py: 0.35,
                borderRadius: 1.5,
                fontWeight: 700,
                color: "primary.dark",
                bgcolor: "rgba(15,118,110,0.1)",
              }}
            >
              Score {formatScore(chunk.score)}
            </Typography>
          </Box>
        )}
      </Box>
    </Box>
  );
}

RetrievedContext.propTypes = {
  chunks: PropTypes.arrayOf(
    PropTypes.shape({
      rank: PropTypes.number,
      content: PropTypes.string,
      source: PropTypes.string,
      score: PropTypes.number,
      metadata: PropTypes.object,
    }),
  ),
};

RetrievedContext.defaultProps = {
  chunks: [],
};

export default RetrievedContext;
