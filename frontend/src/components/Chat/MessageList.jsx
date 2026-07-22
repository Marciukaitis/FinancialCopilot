import { useEffect, useRef } from "react";
import PropTypes from "prop-types";
import Box from "@mui/material/Box";
import CircularProgress from "@mui/material/CircularProgress";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import MessageBubble from "./MessageBubble";

function MessageList({ messages, loading }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  if (!messages.length && !loading) {
    return (
      <Box
        sx={{
          flex: 1,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          px: 3,
        }}
      >
        <Typography color="text.secondary" textAlign="center">
          Hacé una pregunta sobre tus documentos financieros.
          <br />
          Las respuestas se basan únicamente en el contenido indexado.
        </Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ flex: 1, overflowY: "auto", px: { xs: 2, md: 3 }, py: 2 }}>
      {messages.map((message) => (
        <MessageBubble key={message.id} message={message} />
      ))}

      {loading && (
        <Stack direction="row" spacing={1.5} alignItems="center" sx={{ mt: 1 }}>
          <CircularProgress size={18} thickness={5} />
          <Typography variant="body2" color="text.secondary">
            Analizando documentos…
          </Typography>
        </Stack>
      )}

      <div ref={bottomRef} />
    </Box>
  );
}

MessageList.propTypes = {
  messages: PropTypes.arrayOf(PropTypes.object).isRequired,
  loading: PropTypes.bool,
};

MessageList.defaultProps = {
  loading: false,
};

export default MessageList;
