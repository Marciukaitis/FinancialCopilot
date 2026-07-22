import { useEffect, useRef } from "react";
import PropTypes from "prop-types";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import MessageBubble from "./MessageBubble";
import RagPipeline from "./RagPipeline";

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
          background:
            "radial-gradient(circle at 50% 40%, rgba(94,234,212,0.16), transparent 55%)",
        }}
      >
        <Box sx={{ textAlign: "center", maxWidth: 420 }}>
          <Typography
            variant="h6"
            sx={{ mb: 1, fontFamily: '"Syne", sans-serif' }}
          >
            Empezá una consulta
          </Typography>
          <Typography color="text.secondary">
            Elegí una pregunta del panel o escribí la tuya. El copiloto responde
            solo con evidencia de tus PDFs indexados.
          </Typography>
        </Box>
      </Box>
    );
  }

  return (
    <Box sx={{ flex: 1, overflowY: "auto", px: { xs: 2, md: 3 }, py: 2.5 }}>
      {messages.map((message) => (
        <MessageBubble key={message.id} message={message} />
      ))}

      <RagPipeline loading={loading} />

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
