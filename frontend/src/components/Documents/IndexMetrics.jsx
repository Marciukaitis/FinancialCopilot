import PropTypes from "prop-types";
import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";

function shortModel(model) {
  if (!model) return "";
  const parts = model.split("/");
  return parts[parts.length - 1];
}

function IndexMetrics({ status }) {
  const metrics = [
    { label: "Chunks", value: status?.chunks_indexed ?? 0 },
    { label: "Embed", value: shortModel(status?.embedding_model) || "HF ST" },
    { label: "DB", value: status?.vector_db || "Chroma" },
    { label: "LLM", value: status?.llm_model || "llama3.2" },
  ];

  return (
    <Stack
      direction="row"
      spacing={0.75}
      flexWrap="wrap"
      useFlexGap
      sx={{
        px: 1,
        py: 0.75,
        borderRadius: 3,
        bgcolor: "rgba(255,255,255,0.72)",
        border: "1px solid",
        borderColor: "divider",
        backdropFilter: "blur(8px)",
      }}
    >
      {metrics.map((metric) => (
        <Box
          key={metric.label}
          sx={{
            px: 1.1,
            py: 0.55,
            minWidth: 72,
            borderRadius: 2,
            bgcolor: "rgba(15,118,110,0.05)",
            border: "1px solid rgba(15,118,110,0.1)",
          }}
        >
          <Typography
            variant="caption"
            sx={{
              display: "block",
              color: "text.secondary",
              fontWeight: 600,
              fontSize: 10,
              lineHeight: 1.1,
            }}
          >
            {metric.label}
          </Typography>
          <Typography
            variant="body2"
            sx={{
              fontWeight: 700,
              fontSize: 12,
              maxWidth: 110,
              overflow: "hidden",
              textOverflow: "ellipsis",
              whiteSpace: "nowrap",
            }}
            title={String(metric.value)}
          >
            {metric.value}
          </Typography>
        </Box>
      ))}
    </Stack>
  );
}

IndexMetrics.propTypes = {
  status: PropTypes.shape({
    chunks_indexed: PropTypes.number,
    embedding_model: PropTypes.string,
    llm_model: PropTypes.string,
    vector_db: PropTypes.string,
  }),
};

IndexMetrics.defaultProps = {
  status: {},
};

export default IndexMetrics;
