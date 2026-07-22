import { useCallback, useState } from "react";
import { askQuestion } from "../api/client";

export function useChat() {
  const [messages, setMessages] = useState([]);
  const [threadId, setThreadId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const sendMessage = useCallback(
    async (text) => {
      const query = text.trim();
      if (!query || loading) return;

      const userMessage = {
        id: `user-${Date.now()}`,
        role: "user",
        content: query,
      };

      setMessages((prev) => [...prev, userMessage]);
      setLoading(true);
      setError("");

      try {
        const response = await askQuestion(query, threadId);
        setThreadId(response.thread_id);

        const assistantMessage = {
          id: `assistant-${Date.now()}`,
          role: "assistant",
          content: response.answer,
          sources: response.sources || [],
        };

        setMessages((prev) => [...prev, assistantMessage]);
      } catch (err) {
        setError(err.message || "No se pudo obtener una respuesta");
      } finally {
        setLoading(false);
      }
    },
    [loading, threadId],
  );

  const clearChat = useCallback(() => {
    setMessages([]);
    setThreadId(null);
    setError("");
  }, []);

  return {
    messages,
    threadId,
    loading,
    error,
    sendMessage,
    clearChat,
  };
}
