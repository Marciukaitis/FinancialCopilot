import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Grid2";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import ChatPanel from "./components/Chat/ChatPanel";
import DocumentsPanel from "./components/Documents/DocumentsPanel";
import { useChat } from "./hooks/useChat";
import { useDocuments } from "./hooks/useDocuments";

function App() {
  const chat = useChat();
  const documents = useDocuments();

  return (
    <Box
      sx={{
        minHeight: "100vh",
        bgcolor: "background.default",
        backgroundImage:
          "radial-gradient(circle at top left, rgba(31,75,63,0.08), transparent 40%), radial-gradient(circle at bottom right, rgba(196,165,116,0.12), transparent 35%)",
      }}
    >
      <AppBar
        position="sticky"
        color="transparent"
        sx={{
          borderBottom: "1px solid",
          borderColor: "divider",
          bgcolor: "rgba(243,241,236,0.9)",
          backdropFilter: "blur(8px)",
        }}
      >
        <Toolbar>
          <Box sx={{ flexGrow: 1 }}>
            <Typography variant="h5" component="h1">
              Finance Copilot
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Consulta inteligente sobre documentación financiera
            </Typography>
          </Box>
          {chat.threadId && (
            <Typography variant="caption" color="text.secondary">
              Sesión: {chat.threadId.slice(0, 8)}…
            </Typography>
          )}
        </Toolbar>
      </AppBar>

      <Container maxWidth="xl" sx={{ py: { xs: 2, md: 3 } }}>
        <Grid container spacing={2.5} sx={{ minHeight: { md: "calc(100vh - 140px)" } }}>
          <Grid size={{ xs: 12, md: 4 }}>
            <DocumentsPanel
              status={documents.status}
              uploading={documents.uploading}
              error={documents.error}
              lastUploaded={documents.lastUploaded}
              onUpload={documents.upload}
            />
          </Grid>

          <Grid size={{ xs: 12, md: 8 }} sx={{ minHeight: { xs: 560, md: "auto" } }}>
            <ChatPanel
              messages={chat.messages}
              loading={chat.loading}
              error={chat.error}
              onSend={chat.sendMessage}
              onClear={chat.clearChat}
            />
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
}

export default App;
