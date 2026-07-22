import PropTypes from "prop-types";
import CheckCircleRoundedIcon from "@mui/icons-material/CheckCircleRounded";
import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";

function KnowledgeBaseStatus({ status }) {
  const documents = status?.documents?.length ? status.documents : [];
  const indexed = Boolean(status?.indexed);

  return (
    <Box>
      <Stack
        direction="row"
        justifyContent="space-between"
        alignItems="center"
        sx={{ mb: 1 }}
      >
        <Typography
          variant="subtitle2"
          sx={{
            letterSpacing: 0.7,
            textTransform: "uppercase",
            color: "text.secondary",
            fontWeight: 700,
            fontSize: 11,
          }}
        >
          Knowledge Base
        </Typography>
        <Box
          sx={{
            px: 1,
            py: 0.35,
            borderRadius: 2,
            fontSize: 11,
            fontWeight: 700,
            color: indexed ? "#5f7d72" : "#78716c",
            bgcolor: indexed ? "rgba(125,158,143,0.18)" : "rgba(0,0,0,0.04)",
            border: "1px solid",
            borderColor: indexed ? "rgba(125,158,143,0.28)" : "divider",
          }}
        >
          {indexed ? "Indexado" : "Pendiente"}
        </Box>
      </Stack>

      {documents.length === 0 ? (
        <Typography variant="body2" color="text.secondary">
          Sin PDFs todavía.
        </Typography>
      ) : (
        <Stack spacing={0.75}>
          {documents.map((name) => (
            <Stack
              key={name}
              direction="row"
              spacing={0.75}
              alignItems="center"
              sx={{
                px: 1,
                py: 0.7,
                borderRadius: 2,
                bgcolor: "rgba(255,255,255,0.7)",
                border: "1px solid rgba(109,143,136,0.1)",
              }}
            >
              <CheckCircleRoundedIcon sx={{ fontSize: 15, color: "#6d8f88", flexShrink: 0 }} />
              <Typography
                variant="body2"
                fontWeight={500}
                sx={{
                  flex: 1,
                  minWidth: 0,
                  overflow: "hidden",
                  textOverflow: "ellipsis",
                  whiteSpace: "nowrap",
                }}
                title={name}
              >
                {name}
              </Typography>
            </Stack>
          ))}
        </Stack>
      )}
    </Box>
  );
}

KnowledgeBaseStatus.propTypes = {
  status: PropTypes.shape({
    documents: PropTypes.arrayOf(PropTypes.string),
    indexed: PropTypes.bool,
  }),
};

KnowledgeBaseStatus.defaultProps = {
  status: {},
};

export default KnowledgeBaseStatus;
