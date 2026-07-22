import { useMemo, useState } from "react";
import PropTypes from "prop-types";
import ArrowForwardRoundedIcon from "@mui/icons-material/ArrowForwardRounded";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Stack from "@mui/material/Stack";
import Tab from "@mui/material/Tab";
import Tabs from "@mui/material/Tabs";
import Typography from "@mui/material/Typography";
import {
  FOLLOWUP_FLOW,
  OUT_OF_SCOPE_QUESTIONS,
  SAMPLE_QUESTIONS,
} from "../../data/sampleQuestions";

const TABS = [
  { id: "prestamos", label: "Préstamos", tone: "default" },
  { id: "productos", label: "Productos", tone: "default" },
  { id: "procedimientos", label: "Procesos", tone: "default" },
  { id: "memoria", label: "Memoria", tone: "info" },
  { id: "fuera", label: "Fuera", tone: "warning" },
];

function QuestionButton({ question, onSelect, tone, prefix }) {
  return (
    <Button
      fullWidth
      variant="text"
      endIcon={<ArrowForwardRoundedIcon sx={{ fontSize: 15, opacity: 0.5 }} />}
      onClick={() => onSelect(question)}
      sx={{
        justifyContent: "space-between",
        textAlign: "left",
        color: tone === "warning" ? "#92400e" : "text.primary",
        fontWeight: 500,
        px: 1.35,
        py: 1.25,
        minHeight: 48,
        borderRadius: 2.5,
        bgcolor:
          tone === "warning"
            ? "rgba(217,119,6,0.07)"
            : tone === "info"
              ? "rgba(14,165,233,0.07)"
              : "rgba(255,255,255,0.65)",
        border: "1px solid",
        borderColor:
          tone === "warning"
            ? "rgba(217,119,6,0.2)"
            : tone === "info"
              ? "rgba(14,165,233,0.2)"
              : "rgba(15,118,110,0.1)",
        transition: "transform 0.18s ease, background-color 0.18s ease",
        "&:hover": {
          bgcolor:
            tone === "warning"
              ? "rgba(217,119,6,0.12)"
              : tone === "info"
                ? "rgba(14,165,233,0.12)"
                : "rgba(15,118,110,0.08)",
          transform: "translateX(2px)",
        },
      }}
    >
      <Box component="span" sx={{ pr: 1, lineHeight: 1.45, fontSize: "0.9rem" }}>
        {prefix ? (
          <Box component="span" sx={{ fontWeight: 700, mr: 0.6, opacity: 0.7 }}>
            {prefix}
          </Box>
        ) : null}
        {question}
      </Box>
    </Button>
  );
}

QuestionButton.propTypes = {
  question: PropTypes.string.isRequired,
  onSelect: PropTypes.func.isRequired,
  tone: PropTypes.oneOf(["default", "warning", "info"]),
  prefix: PropTypes.string,
};

QuestionButton.defaultProps = {
  tone: "default",
  prefix: "",
};

function SampleQuestions({ onSelect }) {
  const [tab, setTab] = useState("prestamos");
  const active = useMemo(() => TABS.find((item) => item.id === tab) || TABS[0], [tab]);

  const items = useMemo(() => {
    if (tab === "memoria") {
      return FOLLOWUP_FLOW.map((question, index) => ({
        question,
        prefix: `${index + 1}.`,
        tone: "info",
      }));
    }
    if (tab === "fuera") {
      return OUT_OF_SCOPE_QUESTIONS.map((question) => ({
        question,
        tone: "warning",
      }));
    }
    const group = SAMPLE_QUESTIONS[tab];
    return (group?.questions || []).map((question) => ({
      question,
      tone: "default",
    }));
  }, [tab]);

  const hint =
    tab === "memoria"
      ? "Seguí el orden en la misma sesión para probar memoria."
      : tab === "fuera"
        ? "Si no está en los docs, debe decir que no sabe."
        : "Tocá una pregunta para enviarla al chat.";

  return (
    <Box sx={{ display: "flex", flexDirection: "column", flex: 1, minHeight: 0 }}>
      <Tabs
        value={tab}
        onChange={(_, value) => setTab(value)}
        variant="scrollable"
        scrollButtons="auto"
        allowScrollButtonsMobile
        sx={{
          minHeight: 36,
          mb: 1.25,
          "& .MuiTabs-indicator": {
            height: 2.5,
            borderRadius: 2,
            bgcolor: active.tone === "warning" ? "#d97706" : "primary.main",
          },
          "& .MuiTab-root": {
            minHeight: 36,
            minWidth: "auto",
            px: 1.1,
            py: 0.5,
            fontSize: 12,
            fontWeight: 650,
            textTransform: "none",
            color: "text.secondary",
          },
          "& .Mui-selected": {
            color:
              active.tone === "warning"
                ? "#92400e !important"
                : "primary.dark !important",
          },
        }}
      >
        {TABS.map((item) => (
          <Tab key={item.id} value={item.id} label={item.label} />
        ))}
      </Tabs>

      <Typography
        variant="caption"
        color="text.secondary"
        sx={{ display: "block", mb: 1.1, lineHeight: 1.4 }}
      >
        {hint}
      </Typography>

      <Stack spacing={1.5} sx={{ flex: 1, overflowY: "auto", pr: 0.75, pb: 1.5 }}>
        {items.map((item) => (
          <QuestionButton
            key={item.question}
            question={item.question}
            onSelect={onSelect}
            tone={item.tone}
            prefix={item.prefix}
          />
        ))}
      </Stack>
    </Box>
  );
}

SampleQuestions.propTypes = {
  onSelect: PropTypes.func.isRequired,
};

export default SampleQuestions;
