import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Grid2";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import ChatPanel from "./components/Chat/ChatPanel";
import DocumentsPanel from "./components/Documents/DocumentsPanel";
import IndexMetrics from "./components/Documents/IndexMetrics";
import UploadButton from "./components/Documents/UploadButton";
import { useChat } from "./hooks/useChat";
import { useDocuments } from "./hooks/useDocuments";

function App() {
  const chat = useChat();
  const documents = useDocuments();

  return (
    <Box
      sx={{
        minHeight: "100vh",
        height: { md: "100vh" },
        position: "relative",
        overflow: { xs: "auto", md: "hidden" },
        background:
          "radial-gradient(ellipse 80% 50% at 10% -10%, rgba(201,221,215,0.45), transparent 55%), radial-gradient(ellipse 70% 45% at 95% 5%, rgba(196,210,218,0.28), transparent 50%), linear-gradient(180deg, #f7f6f3 0%, #f1f0ec 55%, #ebeae5 100%)",
        "&::before": {
          content: '""',
          position: "absolute",
          inset: 0,
          backgroundImage:
            "linear-gradient(rgba(109,143,136,0.035) 1px, transparent 1px), linear-gradient(90deg, rgba(109,143,136,0.035) 1px, transparent 1px)",
          backgroundSize: "48px 48px",
          maskImage: "radial-gradient(circle at center, black 35%, transparent 85%)",
          pointerEvents: "none",
        },
      }}
    >
      <Container
        maxWidth="xl"
        sx={{
          position: "relative",
          py: { xs: 2, md: 2.5 },
          height: { md: "100%" },
          display: "flex",
          flexDirection: "column",
        }}
      >
        <Stack
          direction={{ xs: "column", md: "row" }}
          justifyContent="space-between"
          alignItems={{ xs: "stretch", md: "center" }}
          spacing={2}
          className="fc-fade-up"
          sx={{ mb: { xs: 2, md: 2.25 }, flexShrink: 0 }}
        >
          <Stack direction="row" spacing={2} alignItems="center">
            <Box
              className="fc-brand-orb"
              sx={{
                width: 48,
                height: 48,
                flexShrink: 0,
                borderRadius: "16px",
                background:
                  "linear-gradient(145deg, #d7e5e1 0%, #9bb5af 55%, #b7c7cf 100%)",
                boxShadow: "0 10px 28px rgba(109,143,136,0.18)",
              }}
            />
            <Box>
              <Typography
                variant="h1"
                sx={{
                  fontSize: { xs: "1.75rem", md: "2.15rem" },
                  lineHeight: 0.95,
                  color: "text.primary",
                }}
              >
                Finance Copilot
              </Typography>
              <Typography
                variant="body2"
                sx={{ mt: 0.55, color: "text.secondary", maxWidth: 420 }}
              >
                RAG local · fuentes trazables · memoria conversacional
              </Typography>
            </Box>
          </Stack>

          <Stack
            direction="row"
            spacing={1.25}
            alignItems="center"
            justifyContent={{ xs: "flex-start", md: "flex-end" }}
            flexWrap="wrap"
            useFlexGap
          >
            {chat.threadId && (
              <Box
                sx={{
                  px: 1.35,
                  py: 0.7,
                  borderRadius: 2,
                  bgcolor: "rgba(109,143,136,0.08)",
                  border: "1px solid",
                  borderColor: "divider",
                }}
              >
                <Typography variant="caption" color="primary.dark">
                  Sesión {chat.threadId.slice(0, 8)}
                </Typography>
              </Box>
            )}

            <IndexMetrics status={documents.status} />

            <UploadButton
              onUpload={documents.upload}
              uploading={documents.uploading}
              error={documents.error}
              lastUploaded={documents.lastUploaded}
            />
          </Stack>
        </Stack>

        <Grid
          container
          spacing={2.25}
          className="fc-fade-up-delay"
          sx={{
            flex: 1,
            minHeight: 0,
            height: { md: "calc(100% - 88px)" },
          }}
        >
          <Grid
            size={{ xs: 12, md: 4 }}
            sx={{
              height: { xs: 420, md: "100%" },
              minHeight: 0,
              display: "flex",
            }}
          >
            <Box sx={{ width: "100%", height: "100%" }}>
              <DocumentsPanel
                status={documents.status}
                onSelectQuestion={chat.sendMessage}
              />
            </Box>
          </Grid>

          <Grid
            size={{ xs: 12, md: 8 }}
            sx={{
              height: { xs: 560, md: "100%" },
              minHeight: 0,
              display: "flex",
            }}
          >
            <Box sx={{ width: "100%", height: "100%" }}>
              <ChatPanel
                messages={chat.messages}
                loading={chat.loading}
                error={chat.error}
                onSend={chat.sendMessage}
                onClear={chat.clearChat}
              />
            </Box>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
}

export default App;
