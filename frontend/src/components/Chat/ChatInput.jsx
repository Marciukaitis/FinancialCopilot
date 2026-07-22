import { useState } from "react";
import PropTypes from "prop-types";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import IconButton from "@mui/material/IconButton";
import InputBase from "@mui/material/InputBase";
import Paper from "@mui/material/Paper";
import Tooltip from "@mui/material/Tooltip";
import SendRoundedIcon from "@mui/icons-material/SendRounded";
import RestartAltRoundedIcon from "@mui/icons-material/RestartAltRounded";

function ChatInput({ onSend, onClear, disabled }) {
  const [value, setValue] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!value.trim() || disabled) return;
    onSend(value);
    setValue("");
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSubmit(event);
    }
  };

  return (
    <Box
      component="form"
      onSubmit={handleSubmit}
      sx={{
        px: { xs: 2, md: 3 },
        py: 2,
        borderTop: "1px solid",
        borderColor: "divider",
        bgcolor: "background.paper",
      }}
    >
      <Paper
        variant="outlined"
        sx={{
          display: "flex",
          alignItems: "flex-end",
          gap: 1,
          px: 1.5,
          py: 1,
          borderColor: "divider",
        }}
      >
        <InputBase
          fullWidth
          multiline
          maxRows={4}
          placeholder="Escribí tu pregunta…"
          value={value}
          onChange={(event) => setValue(event.target.value)}
          onKeyDown={handleKeyDown}
          disabled={disabled}
          sx={{ py: 0.75 }}
        />

        <Tooltip title="Nueva conversación">
          <span>
            <IconButton onClick={onClear} disabled={disabled} aria-label="limpiar chat">
              <RestartAltRoundedIcon />
            </IconButton>
          </span>
        </Tooltip>

        <Button
          type="submit"
          variant="contained"
          disabled={disabled || !value.trim()}
          endIcon={<SendRoundedIcon />}
          sx={{ minWidth: 112, height: 40 }}
        >
          Enviar
        </Button>
      </Paper>
    </Box>
  );
}

ChatInput.propTypes = {
  onSend: PropTypes.func.isRequired,
  onClear: PropTypes.func.isRequired,
  disabled: PropTypes.bool,
};

ChatInput.defaultProps = {
  disabled: false,
};

export default ChatInput;
