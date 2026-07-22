import PropTypes from "prop-types";
import Box from "@mui/material/Box";
import Chip from "@mui/material/Chip";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";

function MessageBubble({ message }) {
  const isUser = message.role === "user";

  return (
    <Box
      sx={{
        display: "flex",
        justifyContent: isUser ? "flex-end" : "flex-start",
        mb: 1.5,
      }}
    >
      <Box
        sx={{
          maxWidth: "78%",
          px: 2,
          py: 1.5,
          borderRadius: 2,
          bgcolor: isUser ? "primary.main" : "background.paper",
          color: isUser ? "primary.contrastText" : "text.primary",
          border: isUser ? "none" : "1px solid",
          borderColor: "divider",
        }}
      >
        <Typography
          variant="caption"
          sx={{
            display: "block",
            mb: 0.5,
            opacity: 0.75,
            letterSpacing: 0.3,
          }}
        >
          {isUser ? "Vos" : "Finance Copilot"}
        </Typography>

        <Typography
          variant="body1"
          sx={{ whiteSpace: "pre-wrap", lineHeight: 1.6 }}
        >
          {message.content}
        </Typography>

        {!isUser && message.sources?.length > 0 && (
          <Stack direction="row" spacing={1} useFlexGap flexWrap="wrap" sx={{ mt: 1.5 }}>
            {message.sources.map((source, index) => (
              <Chip
                key={`${source.document}-${source.page}-${index}`}
                size="small"
                variant="outlined"
                label={`${source.document}${
                  source.page != null ? ` · p. ${source.page}` : ""
                }`}
                sx={{
                  borderColor: "divider",
                  bgcolor: "background.default",
                }}
              />
            ))}
          </Stack>
        )}
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
  }).isRequired,
};

export default MessageBubble;
