import PropTypes from "prop-types";
import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import RetrievedContext from "./RetrievedContext";

function stripEmbeddedSources(content) {
  if (!content) return "";
  const markers = ["\n---\nFuentes:", "\nFuentes:", "\n**Fuentes:**"];
  const lower = content.toLowerCase();
  let cutAt = -1;

  markers.forEach((marker) => {
    const idx = lower.indexOf(marker.toLowerCase());
    if (idx !== -1 && (cutAt === -1 || idx < cutAt)) {
      cutAt = idx;
    }
  });

  return (cutAt === -1 ? content : content.slice(0, cutAt)).trim();
}

function cleanDocumentName(name) {
  if (!name) return "";
  const base = String(name).split(/[/\\]/).pop();
  const match = base.match(/^[0-9a-f]{32}_(.+)$/i);
  return match ? match[1] : base;
}

function dedupeSources(sources) {
  const seen = new Set();
  return (sources || []).filter((source) => {
    const document = cleanDocumentName(source.document);
    const key = `${document}::${source.page ?? "n/a"}`;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

function MessageBubble({ message }) {
  const isUser = message.role === "user";
  const content = isUser
    ? message.content
    : stripEmbeddedSources(message.content);

  return (
    <Box
      className="fc-message-in"
      sx={{
        display: "flex",
        justifyContent: isUser ? "flex-end" : "flex-start",
        mb: 1.75,
      }}
    >
      <Box
        sx={{
          maxWidth: { xs: "96%", md: "88%" },
          px: 2.1,
          py: 1.6,
          borderRadius: isUser ? "18px 18px 6px 18px" : "18px 18px 18px 6px",
          background: isUser
            ? "linear-gradient(135deg, #a8c0ba 0%, #9bb5af 100%)"
            : "rgba(255,255,255,0.95)",
          color: isUser ? "#24302d" : "text.primary",
          border: isUser ? "1px solid rgba(109,143,136,0.18)" : "1px solid rgba(109,143,136,0.12)",
          boxShadow: isUser
            ? "0 8px 20px rgba(109,143,136,0.12)"
            : "0 8px 20px rgba(47,55,53,0.05)",
        }}
      >
        <Typography
          variant="caption"
          sx={{
            display: "block",
            mb: 0.6,
            opacity: 0.78,
            letterSpacing: 0.4,
            fontWeight: 600,
            textTransform: "uppercase",
            fontSize: 10,
          }}
        >
          {isUser ? "Vos" : "Finance Copilot"}
        </Typography>

        <Typography
          variant="body1"
          sx={{ whiteSpace: "pre-wrap", lineHeight: 1.65, fontSize: "0.98rem" }}
        >
          {content}
        </Typography>

        {!isUser && message.sources?.length > 0 && (
          <Box sx={{ mt: 1.5 }}>
            <Typography
              variant="caption"
              sx={{
                display: "block",
                mb: 0.85,
                fontWeight: 700,
                letterSpacing: 0.55,
                textTransform: "uppercase",
                color: "text.secondary",
                fontSize: 10,
              }}
            >
              Sources
            </Typography>
            <Stack direction="row" spacing={1} useFlexGap flexWrap="wrap">
              {dedupeSources(message.sources).map((source, index) => (
                <Box
                  key={`${source.document}-${source.page}-${index}`}
                  sx={{
                    px: 1.1,
                    py: 0.45,
                    borderRadius: 1.5,
                    fontSize: 12,
                    fontWeight: 600,
                    color: "primary.dark",
                    bgcolor: "rgba(109,143,136,0.08)",
                    border: "1px solid rgba(109,143,136,0.14)",
                  }}
                >
                  {cleanDocumentName(source.document)}
                  {source.page != null ? ` · p. ${source.page}` : ""}
                </Box>
              ))}
            </Stack>
          </Box>
        )}

        {!isUser && <RetrievedContext chunks={message.retrievedChunks} />}
      </Box>
    </Box>
  );
}

MessageBubble.propTypes = {
  message: PropTypes.shape({
    role: PropTypes.string.isRequired,
    content: PropTypes.string.isRequired,
    sources: PropTypes.arrayOf(
      PropTypes.shape({
        document: PropTypes.string,
        page: PropTypes.number,
      }),
    ),
    retrievedChunks: PropTypes.arrayOf(PropTypes.object),
  }).isRequired,
};

export default MessageBubble;
