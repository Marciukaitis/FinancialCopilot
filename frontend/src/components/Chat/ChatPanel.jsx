import PropTypes from "prop-types";
import Alert from "@mui/material/Alert";
import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import ChatInput from "./ChatInput";
import MessageList from "./MessageList";

function ChatPanel({ messages, loading, error, onSend, onClear }) {
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
          "linear-gradient(180deg, rgba(251,250,248,0.94) 0%, rgba(247,246,243,0.88) 100%)",
        backdropFilter: "blur(14px)",
        boxShadow: "0 14px 40px rgba(47,55,53,0.06)",
      }}
    >
      <Box
        sx={{
          px: 3,
          py: 2.25,
          borderBottom: "1px solid",
          borderColor: "divider",
          background:
            "linear-gradient(90deg, rgba(201,221,215,0.35), rgba(196,210,218,0.22))",
        }}
      >
        <Stack direction="row" justifyContent="space-between" alignItems="center">
          <Box>
            <Typography variant="h5">Conversación</Typography>
            <Typography variant="body2" color="text.secondary">
              Preguntá en lenguaje natural. Siempre verás documento y página.
            </Typography>
          </Box>
          <Box
            sx={{
              px: 1.25,
              py: 0.5,
              borderRadius: 2,
              bgcolor: "rgba(109,143,136,0.12)",
              color: "primary.dark",
              fontSize: 12,
              fontWeight: 600,
            }}
          >
            Live RAG
          </Box>
        </Stack>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mx: 2, mt: 2, borderRadius: 2 }}>
          {error}
        </Alert>
      )}

      <MessageList messages={messages} loading={loading} />
      <ChatInput onSend={onSend} onClear={onClear} disabled={loading} />
    </Box>
  );
}

ChatPanel.propTypes = {
  messages: PropTypes.arrayOf(PropTypes.object).isRequired,
  loading: PropTypes.bool,
  error: PropTypes.string,
  onSend: PropTypes.func.isRequired,
  onClear: PropTypes.func.isRequired,
};

ChatPanel.defaultProps = {
  loading: false,
  error: "",
};

export default ChatPanel;
