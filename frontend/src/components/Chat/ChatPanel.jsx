import PropTypes from "prop-types";
import Alert from "@mui/material/Alert";
import Box from "@mui/material/Box";
import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";
import ChatInput from "./ChatInput";
import MessageList from "./MessageList";

function ChatPanel({ messages, loading, error, onSend, onClear }) {
  return (
    <Paper
      sx={{
        height: "100%",
        display: "flex",
        flexDirection: "column",
        border: "1px solid",
        borderColor: "divider",
        overflow: "hidden",
      }}
    >
      <Box
        sx={{
          px: 3,
          py: 2,
          borderBottom: "1px solid",
          borderColor: "divider",
        }}
      >
        <Typography variant="h5">Chat</Typography>
        <Typography variant="body2" color="text.secondary">
          Historial de la conversación con memoria por sesión
        </Typography>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mx: 2, mt: 2 }}>
          {error}
        </Alert>
      )}

      <MessageList messages={messages} loading={loading} />
      <ChatInput onSend={onSend} onClear={onClear} disabled={loading} />
    </Paper>
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
